// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as child_process from 'child_process';
import { measureMemory } from 'vm';

function CallPython(input: any): Promise<any> {
    return new Promise((resolve, reject) => {
        const pythonProcess = child_process.spawn('py', ['D:\\Workspace\\childcoding\\middle.py']);
        
        let output = '';
        let error = '';

        pythonProcess.stdin.write(JSON.stringify(input));
        pythonProcess.stdin.end();

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python script exited with code ${code}: ${error}`));
            } else {
                try {
                    const result = JSON.parse(output);
                    resolve(result);
                } catch (err) {
                    reject(new Error(`Failed to parse Python script output: ${(err as Error).message} with raw output is ${output}`));
                }
            }
        });
    });
}
// >test1.getcode
// function ShowHoverMessage(message: any, document: vscode.TextDocument, position: vscode.Position) {
// 	console.log("ShowHoverMessage");
//     const hoverProvider = vscode.languages.registerHoverProvider(
//         { scheme: 'file', language: 'cpp' }, // 这里可以根据需要调整模式
//         {
//             provideHover(doc, pos) {
//                 console.log("=======");
//                 if (pos.line === position.line ) {
//                     let markdownString = new vscode.MarkdownString(message.bug_info);
//                     markdownString.isTrusted = true;
//                     console.log("--position: ",position);
//                     console.log("--bug_info: ", message.bug_info);
//                     return new vscode.Hover(markdownString);
//                 }
//                 return undefined;
//             }
//         }
//     );

//     // Unregister hover provider after showing the message
//     setTimeout(() => {
//         hoverProvider.dispose();
//     }, 7000);  // Dispose after 5 seconds, adjust as needed
// }
//>test1.getcode
function ShowHoverMessage2(context: vscode.ExtensionContext,message: any, document: vscode.TextDocument, position: vscode.Position) {
    console.log("ShowHoverMessage");

    const decorationType = vscode.window.createTextEditorDecorationType({
        after: {
            contentText: ` ${message.bug_info}`,
            backgroundColor: 'red',
            border: '1px solid black',
            margin: '0 0 0 20px',
            width: 'auto'
        }
    });

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const endPosition = new vscode.Position(position.line, document.lineAt(position.line).range.end.character);
        const range = new vscode.Range(endPosition, endPosition);
        editor.setDecorations(decorationType, [range]);

        const commandId = 'extension.closeDecoration';
        if (!vscode.commands.getCommands(true).then(commands => commands.includes(commandId))) {
            const disposable = vscode.commands.registerCommand(commandId, () => {
                decorationType.dispose();
            });
            vscode.commands.executeCommand('setContext', 'decorationVisible', true);
            context.subscriptions.push(disposable);
        }

        
        const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        statusBarItem.command = commandId;
        statusBarItem.text = '$(close) Close Hover';
        statusBarItem.tooltip = 'Close the hover message';
        statusBarItem.show();

        context.subscriptions.push(statusBarItem);
    }
}

export function activate(context: vscode.ExtensionContext) {
	console.log('Congratulations, test1 is now active!');

    let disposable = vscode.commands.registerCommand('test1.getcode', async  () => {
		console.log("Run command test1.getcode");
        // 获取当前活动的编辑器
        const editor = vscode.window.activeTextEditor;

        if (editor) {
            console.log("in editor");
            const document = editor.document;
			const selection = editor.selection;
			const position = selection.active;
			const selectedtext = document.getText(selection);

            // 获取文件内容
            const code = document.getText();
            // vscode.window.showInformationMessage('C++ code fetched: ' + code.substring(0, 100)); // 显示前100个字符

			const input = {
				code: code,
				// Add more fields as needed
			};	

            try {
                // const result = await CallPython(input);
                console.log("source code: ",input);

                const result = 
                [
                    {
                      "bug_id": "1",
                      "bug_row": "1",
                      "bug_info": "Null pointer exception may occur if the object is not instantiated."
                    },
                    {
                      "bug_id": "2",
                      "bug_row": "3",
                      "bug_info": "Possible array index out of bounds exception due to unchecked array access."
                    },
                    {
                      "bug_id": "3",
                      "bug_row": "5",
                      "bug_info": "Potential memory leak due to unclosed resource."
                    },
                    {
                      "bug_id": "4",
                      "bug_row": "7",
                      "bug_info": "Division by zero error if denominator is not validated."
                    }
                ];
                vscode.window.showInformationMessage(`Output: ${JSON.stringify(result)}`);

                for (const bug of result) {
                    const row = parseInt(bug.bug_row, 10) - 1; // 行号从0开始
                    const pos = new vscode.Position(row, document.lineAt(row).range.end.character);
                    ShowHoverMessage2(context, bug, document, pos);
                }

            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${(error as Error).message}`);
            }
        }
    });

    context.subscriptions.push(disposable);

	const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 200);
    statusBarItem.command = 'test1.getcode';
    statusBarItem.text = '$(play) test1';
    statusBarItem.tooltip = 'Compile and Run C++ code With LLM helped';
    statusBarItem.show();

    context.subscriptions.push(statusBarItem);

}

// This method is called when your extension is deactivated
export function deactivate()
{
	console.log("Deactive test1");
}
