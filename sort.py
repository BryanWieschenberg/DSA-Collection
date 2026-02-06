import numpy as np
import random
import sounddevice as sd
import pyglet
from enum import Enum
from Sorter import RealSorter, VisualSorter
import sys
import time
import threading
import logging
import math

logging.disable(logging.CRITICAL)

class Speed(Enum):
    xxs = .7
    xs = 0.07
    s = 0.009
    m = 0.003
    f = 0.001
    u = 0

if len(sys.argv) < 2:
    print("Usage: python sort.py <algorithm> <size: int ?? 128> <speed: Speed ?? m>")
    print("> Algorithms: selection insertion bubble bogo merge quick radix tim heap bitonic comb cycle pancake cocktail_shaker shell gravity odd_even flash")
    print("> Speed: xxs, xs, s, m, l, xl, xxl")
    exit(1)

ALGORITHM = sys.argv[1]
SIZE = 128
SPEED = Speed.m.value

if len(sys.argv) > 2:
    size_arg = sys.argv[2].lower()
    if size_arg.isdigit():
        SIZE = int(size_arg)
    else:
        print(f"Invalid size '{size_arg}', valid: xxs, xs, s, m, l, xl, xxl")
        exit(1)

if len(sys.argv) > 3:
    speed_arg = sys.argv[3].lower()
    if speed_arg in Speed.__members__:
        SPEED = Speed[speed_arg].value
    else:
        print(f"Invalid speed '{speed_arg}', valid: xxs, xs, s, m, l, xl")
        exit(1)

sys.argv = [sys.argv[0]]

import moderngl
import moderngl_window as mglw

class ContinuousAudioGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.target_freq = 0
        self.current_freq = 0
        self.phase = 0
        self.volume = 0
        self.target_volume = 0
        self.active = False
        self.lock = threading.Lock()
        
        self.stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=1,
            callback=self.callback,
            blocksize=1024
        )
        self.stream.start()
        
    def callback(self, outdata, frames, time_info, status):
        with self.lock:
            if not self.active:
                outdata.fill(0)
                return
            
            freq_diff = self.target_freq - self.current_freq
            self.current_freq += freq_diff * 0.3
            
            vol_diff = self.target_volume - self.volume
            self.volume += vol_diff * 0.1
            
            for i in range(frames):
                if self.current_freq > 0:
                    sample = np.sin(self.phase) * 0.5
                    sample += np.sin(self.phase * 2) * 0.25
                    sample += np.sin(self.phase * 3) * 0.125
                    sample += np.sin(self.phase * 4) * 0.0625
                    
                    outdata[i] = sample * self.volume * 0.2
                    self.phase += 2.0 * np.pi * self.current_freq / self.sample_rate
                    if self.phase > 2.0 * np.pi:
                        self.phase -= 2.0 * np.pi
                else:
                    outdata[i] = 0
    
    def set_frequency(self, freq):
        with self.lock:
            self.target_freq = freq
            if not self.active:
                self.current_freq = freq
            self.target_volume = 1.0 if freq > 0 else 0.0
            self.active = freq > 0
    
    def stop(self):
        with self.lock:
            self.target_freq = 0
            self.target_volume = 0
            self.active = False
    
    def close(self):
        self.stream.stop()
        self.stream.close()

class SortVisualizer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = f"{ALGORITHM.replace('_', ' ').title()} Sort"
    window_size = (1280, 720)
    resizable = True

    vertex_shader = '''
        #version 330
        in vec2 in_position;
        in vec3 in_color;
        out vec3 v_color;
        
        void main() {
            gl_Position = vec4(in_position, 0.0, 1.0);
            v_color = in_color;
        }
    '''

    fragment_shader = '''
        #version 330
        in vec3 v_color;
        out vec4 fragColor;
        
        void main() {
            fragColor = vec4(v_color, 1.0);
        }
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        try:
            self.audio = ContinuousAudioGenerator()
        except:
            print("Warning: Audio initialization failed, running without audio")
            self.audio = None
        
        self.wnd.vsync = False
        
        self.prog = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader
        )
        
        self.array_size = SIZE

        self.nums = list(range(1, self.array_size + 1))
        random.shuffle(self.nums)

        # self.nums = [random.randint(1, 100) for _ in range(self.array_size)]

        # self.nums = [
        #     min(self.array_size, int(math.exp(random.random() * math.log(self.array_size))))
        #     for _ in range(self.array_size)
        # ]

        # self.nums = list(range(1, self.array_size + 1))
        # self.nums.reverse()

        self.vertex_data = np.zeros(self.array_size * 6 * 5, dtype='f4')
        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, '2f 3f', 'in_position', 'in_color')]
        )
        
        self.bar_width = 2.0 / self.array_size
        self.bar_positions = np.array([-1.0 + i * self.bar_width for i in range(self.array_size)])
        
        self.sorting = False
        self.sorted = False
        self.current_algo = ALGORITHM
        self.sort_speed = SPEED
        self.time_accumulator = 0.0
        self.highlight_indices = []
        self.final_pass = False
        self.final_index = 0
        self.operation_count = 0
        self.start_time = None
        self.sort_time = 0
        self.elapsed_time = 0.0
        self.final_seen = set()
        self.needs_full_update = True
        self.scale_max = max(self.nums)
        self.sort_time = 0.0
        self.measure_sort_time()
        
        self.sp = " " * 8
        self.label = pyglet.text.Label(
            font_name='Arial',
            font_size=20,
            x=10, y=self.window_size[1] - 30,
            color=(255, 255, 255, 255),
        )

        self.build_vertex_data()

    def on_resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)
        self.bar_width = 2.0 / self.array_size
        self.bar_positions = np.array([-1.0 + i * self.bar_width for i in range(self.array_size)])
        self.needs_full_update = True

        if hasattr(self, "label"):
            self.label.y = height - 30

        self.window_size = (width, height)

    def update_bar(self, idx):
        x = self.bar_positions[idx]
        val = self.nums[idx]
        usable_height = 2.0 - 0.07
        height = (val / self.scale_max) * usable_height
        top_y = -1.0 + height
        
        if idx in self.final_seen:
            color = [0.0, 1.0, 0.0]
        elif idx in self.highlight_indices:
            color = [1.0, 0.0, 0.0]
        else:
            color = [1.0, 1.0, 1.0]
        
        offset = idx * 30
        
        vertices = np.array([
            x, -1.0, *color,
            x + self.bar_width, -1.0, *color,
            x, top_y, *color,
            x + self.bar_width, -1.0, *color,
            x + self.bar_width, top_y, *color,
            x, top_y, *color,
        ], dtype='f4')
        
        self.vertex_data[offset:offset+30] = vertices

    def build_vertex_data(self):
        for i in range(self.array_size):
            self.update_bar(i)
        self.vbo.write(self.vertex_data.tobytes())
        self.needs_full_update = False

    def update_changed_bars(self, indices):
        if self.needs_full_update:
            self.build_vertex_data()
            return
            
        unique_indices = set(indices) | set(self.highlight_indices)
        
        for idx in unique_indices:
            if idx < len(self.nums):
                self.update_bar(idx)
        
        self.vbo.write(self.vertex_data.tobytes())

    def play_tone(self, freq):
        if self.audio:
            self.audio.set_frequency(freq)
    
    def stop_tone(self):
        if self.audio:
            self.audio.stop()
    
    def measure_sort_time(self):
        nums_copy = self.nums.copy()
        start = time.perf_counter()
        getattr(RealSorter, self.current_algo)(nums_copy)
        end = time.perf_counter()
        self.sort_time = end - start

    def on_render(self, timer, frame_time):
        self.ctx.clear(0.1, 0.1, 0.1)
        
        if self.wnd.is_key_pressed(self.wnd.keys.SPACE):
            if not self.sorting and not hasattr(self, 'space_pressed'):
                self.sorting = True
                self.sorted = False
                self.final_seen.clear()
                self.final_pass = False
                self.final_index = 0
                self.start_time = time.time()
                self.elapsed_time = 0.0
                if hasattr(self, 'sort_state'):
                    del self.sort_state
                self.space_pressed = True
        else:
            if hasattr(self, 'space_pressed'):
                del self.space_pressed
                
        if self.sorting or self.final_pass:
            self.time_accumulator += frame_time
            if self.time_accumulator >= self.sort_speed:
                self.time_accumulator = 0.0
                self.sort_step()
        elif not self.sorting and not self.final_pass:
            self.stop_tone()
        
        if self.sorting and self.start_time:
            self.elapsed_time = time.time() - self.start_time

        self.sp = " " * 8
        self.label.text = f"{self.current_algo.replace('_',' ').title()} Sort{self.sp}Input Size: {SIZE}{self.sp}Real Time: {self.sort_time*1000:.3f}ms{self.sp}Visual Time: {self.elapsed_time:.3f}s"
        self.label.draw()
        self.vao.render(moderngl.TRIANGLES)

    def sort_step(self):
        if not self.final_pass:
            if not hasattr(self, 'sort_gen'):
                self.sort_gen = getattr(VisualSorter, self.current_algo)(self.nums)

            try:
                prev_indices = set(self.highlight_indices)
                self.highlight_indices = list(next(self.sort_gen))
                self.operation_count += 1

                changed = prev_indices | set(self.highlight_indices)
                
                if self.highlight_indices:
                    j = self.highlight_indices[0]
                    val = self.nums[j]
                    freq = np.interp(val, [1, self.array_size], [100, 400])
                    self.play_tone(freq)
                else:
                    self.stop_tone()
                
                self.update_changed_bars(changed)
                
            except StopIteration:
                self.sorting = False
                self.sorted = True
                self.elapsed_time = time.time() - self.start_time if self.start_time else 0
                self.start_time = None
                self.stop_tone()

                if hasattr(self, 'sort_gen'):
                    del self.sort_gen

                self.highlight_indices = []
                self.needs_full_update = True
                self.build_vertex_data()

                self.final_pass = True
                self.final_index = 0
                return
        else:
            if self.final_index < len(self.nums):
                i = self.final_index
                self.final_seen.add(i)
                self.highlight_indices = []
                freq = np.interp(self.nums[i], [1, self.array_size], [150, 600])  # Lower frequency range
                self.play_tone(freq)
                self.update_bar(i)
                self.vbo.write(
                    self.vertex_data[i * 30:(i + 1) * 30].tobytes(),
                    offset=i * 30 * 4
                )
                self.final_index += 1
            else:
                self.final_pass = False
                self.highlight_indices = []
                self.stop_tone()
                self.update_changed_bars(set())

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE and not self.sorting:
                self.sorting = True
                self.sorted = False
                if hasattr(self, 'sort_state'):
                    del self.sort_state
    
    def destroy(self):
        if self.audio:
            self.audio.close()
        super().destroy()

SortVisualizer.run()
