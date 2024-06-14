// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as child_process from 'child_process';
import { measureMemory } from 'vm';

function CallPython(input: any): Promise<any> {
    return new Promise((resolve, reject) => {
        const pythonProcess = child_process.spawn('py', ['J:\\24.06.13-Hercules\\middle.py']);
        
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

function ShowHoverMessage(message: any, document: vscode.TextDocument, position: vscode.Position) {
	console.log("ShowHoverMessage");

    const hoverProvider = vscode.languages.registerHoverProvider({ pattern: document.uri.fsPath }, {
        provideHover(document, position) {
			let str=message['message'];
            let markdownString = new vscode.MarkdownString(str);
            markdownString.isTrusted = true;
			console.log(str);
            return new vscode.Hover(markdownString);
			// return new vscode.Hover(str);
        }
    });

    // Manually trigger a hover by creating a hover provider
    vscode.commands.executeCommand('editor.action.showHover', {
        position: position,
        textEditor: vscode.window.activeTextEditor
    });

    // Unregister hover provider after showing the message
    setTimeout(() => {
        hoverProvider.dispose();
    }, 5000);  // Dispose after 5 seconds, adjust as needed
}

// function ShowHoverMessage2(message: any, document: vscode.TextDocument, range: vscode.Range) {
// 	console.log("ShowHoverMessage2");

// 	return new vscode.Hover(message['message'],range);

//     const hoverProvider = vscode.languages.registerHoverProvider({ pattern: document.uri.fsPath }, {
//         provideHover(document, position) {
// 			let str=message['message'];
//             let markdownString = new vscode.MarkdownString(str);
//             markdownString.isTrusted = true;
// 			console.log(str);
//             return new vscode.Hover(markdownString,range);
// 			// return new vscode.Hover(str);
//         }
//     });

//     // Manually trigger a hover by creating a hover provider
//     vscode.commands.executeCommand('editor.action.showHover', {
//         range: vscode.Range,
//         textEditor: vscode.window.activeTextEditor
//     });

//     // Unregister hover provider after showing the message
//     setTimeout(() => {
//         hoverProvider.dispose();
//     }, 5000);  // Dispose after 5 seconds, adjust as needed
// }

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	console.log('Congratulations, test1 is now active!');

    let disposable = vscode.commands.registerCommand('test1.getcode', async  () => {
		console.log("Run command test1.getcode");
        // 获取当前活动的编辑器
        const editor = vscode.window.activeTextEditor;

        if (editor) {
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
                const result = await CallPython(input);
                vscode.window.showInformationMessage(`Output: ${JSON.stringify(result)}`);
				
				ShowHoverMessage(result, document,position);
				// ShowHoverMessage2(result,document,new vscode.Range(new vscode.Position(1, 0),new vscode.Position(5,0)));
				// ShowHoverMessage(result, document, new vscode.Position(1,1));
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
