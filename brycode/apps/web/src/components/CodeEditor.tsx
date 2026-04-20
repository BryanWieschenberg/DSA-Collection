import { useCallback, useMemo } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { acceptCompletion, autocompletion } from "@codemirror/autocomplete";
import { githubDark } from "@uiw/codemirror-theme-github";
import { indentUnit } from "@codemirror/language";
import { EditorState, Prec } from "@codemirror/state";
import { keymap } from "@codemirror/view";

interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
  onSubmit?: () => void;
}

export default function CodeEditor({ code, onChange, onSubmit }: CodeEditorProps) {
  const handleChange = useCallback(
    (value: string) => {
      onChange(value);
    },
    [onChange]
  );

  const customKeymap = useMemo(
    () =>
      Prec.highest(
        keymap.of([
          {
            key: "Ctrl-Enter",
            mac: "Cmd-Enter",
            run: () => {
              onSubmit?.();
              return true; // consume the event, prevent newline
            },
          },
          {
            key: "Tab",
            run: acceptCompletion,
          },
        ])
      ),
    [onSubmit]
  );

  return (
    <div className="flex flex-col h-full bg-surface-800 overflow-hidden">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-border">
        <div className="flex items-center gap-2.5">
          {/* Python language indicator */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-surface-600 border border-border">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2C6.48 2 6 4.02 6 5.5V8h6v1H5.5C3.02 9 2 11.02 2 13.5S3.02 18 5.5 18H8v-2.5C8 13.02 9.52 11 12 11h4c1.98 0 3-1.52 3-3.5V5.5C19 3.02 17.48 2 15.5 2H12z"
                fill="#3776AB"
              />
              <path
                d="M12 22c5.52 0 6-2.02 6-3.5V16h-6v-1h6.5c2.48 0 3.5-2.02 3.5-4.5S20.98 6 18.5 6H16v2.5c0 2.48-1.52 4.5-4 4.5h-4c-1.98 0-3 1.52-3 3.5v2c0 2.48 1.52 3.5 3.5 3.5H12z"
                fill="#FFD43B"
              />
              <circle cx="9.5" cy="5.5" r="1" fill="#FFD43B" />
              <circle cx="14.5" cy="18.5" r="1" fill="#3776AB" />
            </svg>
            <span className="text-[12px] font-medium text-text-secondary">
              Python 3
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Reset button */}
          <button
            id="btn-reset-code"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-text-muted hover:text-text-secondary hover:bg-surface-600 transition-all duration-200 text-[12px] font-medium cursor-pointer"
            title="Reset to starter code"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reset
          </button>
        </div>
      </div>

      {/* CodeMirror editor */}
      <div className="flex-1 overflow-hidden">
        <CodeMirror
          value={code}
          onChange={handleChange}
          extensions={[
            python(),
            indentUnit.of("    "),
            EditorState.tabSize.of(4),
            customKeymap,
            autocompletion({
              activateOnTyping: true,
            }),
          ]}
          theme={githubDark}
          basicSetup={{
            lineNumbers: true,
            highlightActiveLineGutter: true,
            highlightActiveLine: true,
            foldGutter: true,
            dropCursor: true,
            allowMultipleSelections: true,
            indentOnInput: true,
            bracketMatching: true,
            closeBrackets: true,
            autocompletion: true,
            highlightSelectionMatches: true,
            searchKeymap: true,
          }}
          style={{ height: "100%" }}
        />
      </div>
    </div>
  );
}
