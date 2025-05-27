function print_item() {
    
    var printContents = document.getElementById('modal-body').innerHTML;
    


    var printFrame = document.createElement('iframe');

    printFrame.style.position = 'absolute';
    printFrame.style.top = '-1000px';


    document.body.appendChild(printFrame)


    var printDoc = printFrame.contentWindow.document;

    printDoc.open();

    printDoc.write(
        `<html>
            <head>
                <link rel="stylesheet" href="/static/css/styles.css">
                <style>
                    .printcont {
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        flex-direction:column;
                    }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">Test</h1>
                <div class="printcont">
                    ${printContents}
                </div>
            </body>
        </html>`
    );


    printDoc.close()

    printFrame.onload = function() {
        printFrame.contentWindow.focus();
        printFrame.contentWindow.print()


        printFrame.contentWindow.onafterprint = function() {
            document.body.removeChild(printFrame);
        };
    };


}