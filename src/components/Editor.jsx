import MonacoEditor from "@monaco-editor/react";
import { pythonMonarch } from "../lib/pyMonarch";
import { keywords, dsaBuiltins, dsaImports, dsaTypes } from "../lib/pyInfo";

export default function Editor({ value, onChange, onMount }) {
    const handleEditorDidMount = (editor, monaco) => {
        monaco.languages.register({ id: "python-dsa" });
        monaco.languages.setLanguageConfiguration("python-dsa", {
            comments: {
                lineComment: "#",
            },
            brackets: [
                ["{", "}"],
                ["[", "]"],
                ["(", ")"],
            ],
            autoClosingPairs: [
                { open: "{", close: "}" },
                { open: "[", close: "]" },
                { open: "(", close: ")" },
                { open: '"', close: '"' },
                { open: "'", close: "'" },
            ],
            onEnterRules: [
                {
                    beforeText: /:\s*$/,
                    action: { indentAction: monaco.languages.IndentAction.Indent },
                },
            ],
        });
        monaco.editor.defineTheme("dsa-dark-theme", {
            base: "vs-dark",
            inherit: true,
            rules: [
                { token: "keyword.control", foreground: "C586C0" },
                { token: "keyword", foreground: "569CD6" },
                { token: "type", foreground: "4EC9B0" },
                { token: "variable.predefined", foreground: "9CDCFE" },
                { token: "constant", foreground: "569CD6" },
                { token: "entity.name.function", foreground: "DCDCAA" },
                { token: "entity.name.class", foreground: "4EC9B0" },
                { token: "string", foreground: "CE9178" },
                { token: "comment", foreground: "6A9955", fontStyle: "italic" },
                { token: "number", foreground: "B5CEA8" },
            ],
            colors: {
                "editor.background": "#1e1e1e",
            },
        });
        monaco.languages.setMonarchTokensProvider("python-dsa", pythonMonarch);
        monaco.editor.setTheme("dsa-dark-theme");
        monaco.languages.registerCompletionItemProvider("python-dsa", {
            provideCompletionItems: (model, position) => {
                const word = model.getWordUntilPosition(position);
                const range = {
                    startLineNumber: position.lineNumber,
                    endLineNumber: position.lineNumber,
                    startColumn: word.startColumn,
                    endColumn: word.endColumn,
                };
                const text = model.getValue();
                const wordRegex = /[a-zA-Z_]\w*/g;
                const words = new Set();
                let match;
                while ((match = wordRegex.exec(text)) !== null) {
                    words.add(match[0]);
                }
                words.delete(word.word);
                const reserved = new Set([
                    ...keywords,
                    ...dsaBuiltins,
                    ...dsaImports,
                    ...dsaTypes,
                    "self",
                ]);
                const documentSuggestions = Array.from(words)
                    .filter((w) => !reserved.has(w))
                    .map((w) => ({
                        label: w,
                        kind: monaco.languages.CompletionItemKind.Variable,
                        insertText: w,
                        range: range,
                    }));
                const suggestions = [
                    ...documentSuggestions,
                    ...keywords.map((kw) => ({
                        label: kw,
                        kind: monaco.languages.CompletionItemKind.Keyword,
                        insertText: kw,
                        range: range,
                    })),
                    ...dsaBuiltins.map((bi) => ({
                        label: bi,
                        kind: monaco.languages.CompletionItemKind.Function,
                        insertText: bi + "($0)",
                        insertTextRules:
                            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        range: range,
                    })),
                    ...dsaImports.map((item) => ({
                        label: item,
                        kind: ["inf", "nan"].includes(item)
                            ? monaco.languages.CompletionItemKind.Value
                            : monaco.languages.CompletionItemKind.Function,
                        insertText: ["inf", "nan"].includes(item) ? item : item + "($0)",
                        insertTextRules: ["inf", "nan"].includes(item)
                            ? undefined
                            : monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        range: range,
                    })),
                    ...dsaTypes.map((t) => ({
                        label: t,
                        kind: monaco.languages.CompletionItemKind.Class,
                        insertText: t,
                        range: range,
                    })),
                    {
                        label: "def",
                        kind: monaco.languages.CompletionItemKind.Snippet,
                        insertText: "def ${1:method_name}(self, ${2:args}):\n\t${3:pass}\n$0",
                        insertTextRules:
                            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        documentation: "Define a class method",
                        range: range,
                    },
                    {
                        label: "class",
                        kind: monaco.languages.CompletionItemKind.Snippet,
                        insertText:
                            "class ${1:ClassName}:\n\tdef __init__(self):\n\t\t${2:pass}\n$0",
                        insertTextRules:
                            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        documentation: "Define a class with initializer",
                        range: range,
                    },
                ];

                return { suggestions };
            },
        });

        if (onMount) {
            onMount(editor, monaco);
        }
    };

    return (
        <MonacoEditor
            height="100%"
            defaultLanguage="python-dsa"
            language="python-dsa"
            value={value}
            onChange={onChange}
            theme="dsa-dark-theme"
            onMount={handleEditorDidMount}
            options={{
                minimap: { enabled: false },
                tabSize: 4,
                fontFamily: '"Fira Sans Mono", "Fira Mono", "JetBrains Mono", monospace',
                glyphMargin: false,
                lineNumbersMinChars: 3,
                fontSize: 15,
                scrollBeyondLastLine: false,
                padding: { top: 16 },
            }}
        />
    );
}
