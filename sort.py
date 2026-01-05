import numpy as np
import random
import pygame
import pyglet
from enum import Enum
from Sorter import Sorter
import sys
import time

class Speed(Enum):
    xxs = 1; xxsmall = 1;
    xsmall = 0.07; xs = 0.07;
    s = 0.009; small = 0.009
    m = 0.003; medium = 0.003
    l = 0.001; large = 0.001
    f = 0.001; fast = 0.001
    xl = 0; xlarge = 0
    xf = 0; xfast = 0
    u = 0; uncapped = 0; unlimited = 0

class Size(Enum):
    xxxs = 7; xxxsmall = 7
    xxs = 10; xxsmall = 10
    xs = 25; xsmall = 25
    s = 50; small = 50
    m = 100; medium = 100
    l = 250; large = 250
    xl = 500; xlarge = 500
    xxl = 1000; xxlarge = 1000
    xxxl = 2000; xxxlarge = 2000

if len(sys.argv) < 2:
    print("Usage: python sort_visualizer.py <algorithm> <size ?? m> <speed ?? m>")
    print("> Algorithms: bogo, bubble, selection, insertion, merge, quick, heap, counting, bucket, radix, shell, tim, bitonic, introspective, bogo, gnome, cocktail_shaker, comb")
    print("> Sizes/Speeds: xxs, xs, s, m, l, xl")
    exit(1)

ALGORITHM = sys.argv[1]
SIZE = Size.medium.value
SPEED = Speed.medium.value

if len(sys.argv) > 2:
    size_arg = sys.argv[2].lower()
    if size_arg in Size.__members__:
        SIZE = Size[size_arg].value
    else:
        print(f"Invalid size '{size_arg}', valid: xxs, xs, s, m, l, xl")
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
        
        # Initialize pygame mixer for audio
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Stereo output
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)  # Multiple channels for smooth playback
        
        self.wnd.vsync = False
        
        self.prog = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader
        )
        
        self.array_size = SIZE
        self.nums = list(range(1, self.array_size + 1))
        random.shuffle(self.nums)
        
        self.vertex_data = np.zeros(self.array_size * 6 * 5, dtype='f4')
        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, '2f 3f', 'in_position', 'in_color')]
        )
        
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
        self.elapsed_time = 0.0
        self.final_seen = set()

        # Audio optimization
        self.sample_rate = 44100
        self.audio_duration = 0.03
        self.sound_cache = {}
        self.last_sound_time = 0
        
        self.label = pyglet.text.Label(
            f"{self.current_algo.replace('_',' ').title()} Sort        Input Size: {SIZE}        Operations: {self.operation_count}        Time: {self.elapsed_time:.3f}s",
            font_name='Arial',
            font_size=20,
            x=10, y=self.window_size[1] - 30,
            color=(255, 255, 255, 255),
        )

        self.build_vertex_data()

    def on_resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)
        self.build_vertex_data()

        if hasattr(self, "label"):
            self.label.y = height - 30

        self.window_size = (width, height)

    def build_vertex_data(self):
        bar_width = 2.0 / self.array_size
        idx = 0
        
        for i, val in enumerate(self.nums):
            x = -1.0 + i * bar_width
            height = (val / self.array_size) * 2.0

            if i in self.final_seen:
                color = [0.0, 1.0, 0.0]
            elif i in self.highlight_indices:
                color = [1.0, 0.0, 0.0]
            else:
                color = [1.0, 1.0, 1.0]
            
            vertices = [
                [x, -1.0, *color],
                [x + bar_width, -1.0, *color],
                [x, -1.0 + height, *color],
                [x + bar_width, -1.0, *color],
                [x + bar_width, -1.0 + height, *color],
                [x, -1.0 + height, *color],
            ]
            
            for vert in vertices:
                self.vertex_data[idx:idx+5] = vert
                idx += 5
        
        self.vbo.write(self.vertex_data.tobytes())

    def generate_tone(self, freq):
        """Generate a tone and cache it as a pygame Sound object"""
        freq_key = int(freq)
        
        if freq_key not in self.sound_cache:
            # Generate waveform
            samples = int(self.sample_rate * self.audio_duration)
            t = np.linspace(0, self.audio_duration, samples, False)
            
            # Create sine wave with fade out to prevent clicking
            wave = np.sin(freq * t * 2 * np.pi)
            
            # Apply fade envelope (quick fade out at end)
            fade_samples = int(samples * 0.1)  # Last 10% fades out
            fade = np.ones(samples)
            fade[-fade_samples:] = np.linspace(1, 0, fade_samples)
            wave = wave * fade
            
            # Convert to 16-bit stereo
            audio = (wave * 32767 * 0.5).astype(np.int16)  # 50% volume
            stereo = np.repeat(audio.reshape(-1, 1), 2, axis=1)
            
            # Create pygame Sound object
            sound = pygame.sndarray.make_sound(stereo)
            
            self.sound_cache[freq_key] = sound
            
            # Limit cache size
            if len(self.sound_cache) > 100:
                # Remove oldest entry
                self.sound_cache.pop(next(iter(self.sound_cache)))
        
        return self.sound_cache[freq_key]

    def play_tone(self, freq):
        """Play a tone using pygame mixer"""
        try:
            sound = self.generate_tone(freq)
            # Play on any available channel
            sound.play()
        except Exception as e:
            pass  # Silently fail if audio doesn't work
    
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
        
        if self.sorting and self.start_time:
            self.elapsed_time = time.time() - self.start_time

        self.label.text = f"{self.current_algo.replace('_',' ').title()} Sort        Input Size: {SIZE}        Operations: {self.operation_count}        Time: {self.elapsed_time:.3f}"
        self.label.draw()
        self.vao.render(moderngl.TRIANGLES)

    def sort_step(self):
        if not self.final_pass:
            if not hasattr(self, 'sort_gen'):
                self.sort_gen = getattr(Sorter, self.current_algo)(self.nums)

            try:
                self.highlight_indices = list(next(self.sort_gen))
                self.operation_count += 1

                if self.highlight_indices:
                    j = self.highlight_indices[0]
                    val = self.nums[j]
                    freq = np.interp(val, [1, self.array_size], [150, 1200])
                    self.play_tone(freq)
                self.build_vertex_data()
            except StopIteration:
                self.sorting = False
                self.sorted = True
                self.elapsed_time = time.time() - self.start_time if self.start_time else 0
                self.start_time = None

                if hasattr(self, 'sort_gen'):
                    del self.sort_gen
                self.final_pass = True
                self.final_index = 0
                self.highlight_indices = []
                self.build_vertex_data()
                return
        else:
            if self.final_index < len(self.nums):
                i = self.final_index
                self.final_seen.add(i)
                self.highlight_indices = []
                freq = np.interp(self.nums[i], [1, self.array_size], [150, 1200])
                self.play_tone(freq)
                self.build_vertex_data()
                self.final_index += 1
            else:
                self.final_pass = False
                self.highlight_indices = []
                self.build_vertex_data()

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE and not self.sorting:
                self.sorting = True
                self.sorted = False
                if hasattr(self, 'sort_state'):
                    del self.sort_state
    
    def destroy(self):
        """Cleanup on exit"""
        try:
            pygame.mixer.stop()
            self.sound_cache.clear()
            pygame.mixer.quit()
        except:
            pass
        super().destroy()

SortVisualizer.run()