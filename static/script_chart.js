function drawChart(data) {
    const newDivChatRL = document.createElement("div");
    newDivChatRL.classList.add('chat-l');
    const newDivMessL = document.createElement("div");
    newDivMessL.classList.add('mess');
    newDivMessL.classList.add('mess-l');
    newDivMessL.classList.add('span-on-left');
    const newDivSpL = document.createElement("div");
    newDivSpL.classList.add('sp');
    const newSpanL = document.createElement("div");
    
    ////////////////////////////////////////////////////
    if (data["make_graph"] == "yes") {
        newSpanL.classList.add('graph');
        if (data["graph_type"] == "line" || data["graph_type"] == "column") {
            drawColumnGraph(newSpanL, data);
        }
        else if (data["graph_type"] == "table") {
            drawTableChart(newSpanL, data);
        }
        else if (data["graph_type"] == "combo") {
            drawComboChart(newSpanL, data);
        }
    }
    
    ///////////////////////////////////////////////////
    newDivChatRL.appendChild(newDivMessL);
    newDivChatRL.appendChild(newDivSpL);
    if(data["message"] != " "){
        if(data["message"] != ""){
            const newTextL = document.createElement("span");
            newTextL.classList.add('div-shadow-left');
            newTextL.innerHTML = data["message"];
            newDivMessL.appendChild(newTextL);
            newTextL.scrollIntoView();
        }
    }
    if(data["message"] == " " && data["make_graph"] == "no"){
        const newTextL = document.createElement("span");
        newTextL.classList.add('div-shadow-left');
        newTextL.innerHTML = "Sorry no data found";
        newDivMessL.appendChild(newTextL);
    }
    newDivMessL.appendChild(newSpanL);

    const newDivChatRAddL = document.querySelector(".chat-box");
    newDivChatRAddL.appendChild(newDivChatRL);
    newSpanL.scrollIntoView();
    

}



function drawTableChart(divelm, data) {
    const newdiv = document.createElement("div");
    newdiv.classList.add('div-class');
    divelm.appendChild(newdiv);

    google.charts.load('current', { 'packages': ['table'] });
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var dataTable = new google.visualization.DataTable();
        for (let column of data.columns) {
            dataTable.addColumn(column[0], column[1]);
        }
        // Adding rows
        dataTable.addRows(data.rows);
        let vMaxValue = dataTable.getColumnRange(1).max;
        vMaxValue += vMaxValue * .1;
        let table = new google.visualization.Table(newdiv);
        table.draw(dataTable, { showRowNumber: true, width: '100%', height: '100%' });
    }

}

function drawComboChart(divelm, data) {
    const newdiv = document.createElement("div");
    newdiv.classList.add('div-class');
    divelm.appendChild(newdiv);
    google.charts.load('current', { 'packages': ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);
    console.log(data.columns);
    function drawChart() {
        var dataTable = new google.visualization.DataTable();
        for (let column of data.columns) {
            dataTable.addColumn(column[0], column[1]);
        }
        // Adding rows
        dataTable.addRows(data.rows);
        let vMaxValue = dataTable.getColumnRange(1).max;
        vMaxValue *= 1.1;
        let v2MaxValue = dataTable.getColumnRange(0).max;
        v2MaxValue *= 1.1;

        let chartOptions = {
            annotations: {
                textStyle: { color: '#00ff00', bold: true, opacity: 2 }
            },
            // backgroundColor: linear-gradient( 90deg , rgba(242,254,253,1) 0%, rgb(239 250 255) 50%, rgb(229 250 255) 100%),
            backgroundColor:{ gradient: {

                color1: '#f2fefd',

                color2: '#effaff',
                color3: '#e5faff',

                x1: '0%', y1: '0%',
                x2: '50%', y2: '50%',
                x3: '100%', y3: '100%',

            }},
            hAxis: { title: data.columns[0][1] },
            vAxis: { 0: { title: data.columns[1][1], maxValue: vMaxValue }, 1: { title: data.columns[0][1], maxValue: v2MaxValue } },
            seriesType: 'bars',
            series: { 0: { type: 'bars', targetAxisIndex: 0 }, 1: { type: 'line', targetAxisIndex: 1, color: "#ff3333" } },
            legend: "none",
            width: 800,
            height: 400,
            animation: {
                "duration": 600,
                "easing": 'in',
                "startup": true,
                
            },
            // pointShape:"triangle",
            // series : pointSeries,
            chartArea: {
                'width': '80%',
                'height': '60%',
                backgroundColor: {

                    gradient: {

                        color1: '#e1f3f2',
                        color2: '#dcecf3',
                        color3: '#c8ebf3',

                        x1: '0%', y1: '0%',
                        x2: '50%', y2: '50%',
                        x3: '100%', y3: '100%',

                    }
                }, fillOpacity: .001
            }
        }
        let chart = new google.visualization.ComboChart(newdiv);
        chart.draw(dataTable, chartOptions);
    }
}


function drawColumnGraph(divelm, data) {
    const newdiv = document.createElement("div");
    newdiv.classList.add('div-class');
    divelm.appendChild(newdiv);
    google.charts.load('current', { 'packages': ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var dataTable = new google.visualization.DataTable();
        let chartColumns = data["columns"];
        let chartRows = data["rows"];
        for (let i = 0; i < 2; i++) {
            column = chartColumns[i]
            dataTable.addColumn(column[0], column[1]);
        }
        dataTable.addColumn({ type: 'string', role: 'tooltip' });
        // dataTable.addColumn({type: chartColumns[1][0], role: 'annotation'});

        // Adding rows
        let dataTableRows = []
        for (let row of chartRows) {
            let tooltip = "";
            for (let singleRowIndex = 0; singleRowIndex < row.length; singleRowIndex++) {
                let currentColumnData = chartColumns[singleRowIndex]
                let currentColumn = currentColumnData[1];
                let currentRowField = row[singleRowIndex];
                if (currentColumnData[0] == "date") {
                    currentRowField = currentRowField.toDateString()
                }
                tooltip += currentColumn + ": " + currentRowField + "\n"
            }
            dataTableRows.push([row[0], row[1], tooltip]);
        }
        dataTable.addRows(dataTableRows);
        let vMaxValue = dataTable.getColumnRange(1).max;
        vMaxValue += vMaxValue * .1;
        let chartOptions = {
            annotations: {
                textStyle: { color: 'gray', bold: true, opacity: 2 }
            },
            backgroundColor:{ gradient: {

                color1: '#f2fefd',

                color2: '#effaff',
                color3: '#e5faff',

                x1: '0%', y1: '0%',
                x2: '50%', y2: '50%',
                x3: '100%', y3: '100%',

            }},
            hAxis: { title: data.columns[0][1], gridlines: { count: 0 }, slantedText: true, slantedTextAngle: 45 },
            vAxis: { title: data.columns[1][1], maxValue: vMaxValue, gridlines: { count: 0 } },
            legend: "none",
            // pointShape:"triangle",
            // series : pointSeries,
            width: 800,
            height: 400,
            animation: {
                "duration": 600,
                "easing": 'in',
                "startup": true,
                
            },
            chartArea: {
                'width': '80%',
                'height': '80%',
                backgroundColor: {

                    gradient: {

                        color1: '#e1f3f2',
                        color2: '#dcecf3',
                        color3: '#c8ebf3',

                        x1: '0%', y1: '0%',
                        x2: '50%', y2: '50%',
                        x3: '100%', y3: '100%',

                    }
                }, fillOpacity: .001
            },
        }

        if (data["graph_type"] == "line") {
            let chart = new google.visualization.LineChart(newdiv);

            chart.draw(dataTable, chartOptions);
        }
        else if (data["graph_type"] == "column") {
            let chart = new google.visualization.ColumnChart(newdiv);
            chart.draw(dataTable, chartOptions);
        }
    }
}
