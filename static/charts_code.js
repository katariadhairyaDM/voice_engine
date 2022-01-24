function drawChart() {
  let dataColumns = filteredData[0];
  // Iterating through the whole data
  for (let i = 1; i < filteredData.length; i++) {
    let dataRow = filteredData[i];
    console.log(dataRow)
    // Checking if recommedation is dismissed(incorrect)
    let execution = dataRow[dataColumns.indexOf("Status")];
    if (execution == "Incorrect") {
      continue;
    }
    let message = dataRow[dataColumns.indexOf("Message")];
    let dataJSON = dataRow[dataColumns.indexOf("Data JSON")];
    try {
      dataJSON = JSON.parse(dataJSON);
    } catch (e) {
      continue;
    }
    if (message == "NO_MESSAGE_TO_SHOW") {
      continue;
    }
    let cardDiv = document.createElement("div");
    cardDiv.classList.add("card");
    let br = document.createElement("br");
    cardDiv.appendChild(br);


    // Appending div to correct tab
    let divToAppendCard;
    if (dataRow[dataColumns.indexOf("Alert Type")] == "decline") {
      divToAppendCard = "declineDiv"
    }
    else if (dataRow[dataColumns.indexOf("Alert Type")] == "opportunities") {
      divToAppendCard = "opportunitiesDiv"
    }
    else if (dataRow[dataColumns.indexOf("Alert Type")] == "insights") {
      divToAppendCard = "insightsDiv"
    }
    document.getElementById(divToAppendCard).appendChild(cardDiv);
    // Space between cards
    let spaceBetweenCardsBr = document.createElement("br");
    document.getElementById(divToAppendCard).appendChild(spaceBetweenCardsBr);
    // Dismiss card button
    let dismissButton = document.createElement("button");
    dismissButton.innerHTML = "&times;";
    dismissButton.classList.add("crossButton");
    cardDiv.appendChild(dismissButton);
    dismissButton.addEventListener("click", function () {
      for (let i = 1; i < telegramData.length; i++) {
        let row = telegramData[i];
        if (row == dataRow) {
          let rowToCheckInSheet = row.slice();
          google.script.run.withSuccessHandler(function () {
            // Functions coming soon
          }).withFailureHandler(function () {

          }).makeRecommedationIncorrect(rowToCheckInSheet);
          telegramData[i][dataColumns.indexOf("Status")] = "Incorrect";
        }
      }
      cardDiv.remove();
      spaceBetweenCardsBr.remove();
    })
    // Message
    let messagep = document.createElement("p");
    messagep.classList.add("chartMessage")
    messagep.innerHTML = message;
    cardDiv.appendChild(messagep);

    // Checking if we need graph
    if (dataJSON["make_graph"] != "yes") {
      // Lower br
      let lowerBr = document.createElement("br");
      cardDiv.appendChild(lowerBr);
      continue;
    }
    let chartDiv = document.createElement("div");
    chartDiv.classList.add("chartDiv");
    cardDiv.appendChild(chartDiv);
    let chartColumns = dataJSON["axis_types"];
    let chartRows = dataJSON["axis_values_x_y"];
    // Checking if type of column is data
    for (let colInd = 0; colInd < chartColumns.length; colInd++) {
      if (chartColumns[colInd][0] == "date") {
        for (let rowInd = 0; rowInd < chartRows.length; rowInd++) {
          chartRows[rowInd][colInd] = new Date(chartRows[rowInd][colInd]);
        }
      }
    }

    // Making the exact type of chart
    if (dataJSON["type"] == "line" || dataJSON["type"] == "column") {
      // Making date table for chart
      let dataTable = new google.visualization.DataTable();
      // Adding columns
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
        backgroundColor: { gradient: { color1: '#fff8f1', color2: '#f7fcff', x1: '0%', y1: '0%', x2: '100%', y2: '100%' } },
        hAxis: { title: dataJSON["hAxis"], gridlines: { count: 0 }, slantedText: true, slantedTextAngle: 45 },
        vAxis: { title: dataJSON["vAxis"], maxValue: vMaxValue, gridlines: { count: 0 } },
        legend: "none",
        // pointShape:"triangle",
        // series : pointSeries,
        chartArea: {
          'width': '80%',
          'height': '80%',
          backgroundColor: {

            gradient: {

              color1: '#87ceeb',

              color2: '#FFC0CB',

              x1: '0%', y1: '0%',

              x2: '100%', y2: '100%',

            }
          }, fillOpacity: .001
        },
      }

      if (dataJSON["type"] == "line") {
        let chart = new google.visualization.LineChart(chartDiv);

        chart.draw(dataTable, chartOptions);
      }
      else if (dataJSON["type"] == "column") {
        let chart = new google.visualization.ColumnChart(chartDiv);
        chart.draw(dataTable, chartOptions);
      }
    }
    else if (dataJSON["type"] == "combo") {
      // Making date table for chart
      let dataTable = new google.visualization.DataTable();
      // Adding columns
      for (let column of chartColumns) {
        dataTable.addColumn(column[0], column[1]);
      }
      // Adding rows
      dataTable.addRows(chartRows);
      let vMaxValue = dataTable.getColumnRange(1).max;
      vMaxValue *= 1.1;
      let v2MaxValue = dataTable.getColumnRange(2).max;
      v2MaxValue *= 1.1;

      let chartOptions = {
        backgroundColor: { gradient: { color1: '#fff8f1', color2: '#f7fcff', x1: '0%', y1: '0%', x2: '100%', y2: '100%' } },
        hAxis: { title: dataJSON["hAxis"], gridlines: { count: 0 } },
        vAxis: { 0: { title: dataJSON["vAxis"], maxValue: vMaxValue }, 1: { title: dataJSON["vAxis"], maxValue: v2MaxValue } },
        seriesType: 'bars',
        series: { 0: { type: 'bars', targetAxisIndex: 0 }, 1: { type: 'line', targetAxisIndex: 1, color: "#ff3333" } },
        legend: "none",
        // pointShape:"triangle",
        // series : pointSeries,
        chartArea: {
          'width': '80%',
          'height': '60%',
          backgroundColor: {

            gradient: {

              color1: '#87ceeb',

              color2: '#FFC0CB',

              x1: '0%', y1: '0%',

              x2: '100%', y2: '100%',

            }
          }, fillOpacity: .001
        }
      }
      let chart = new google.visualization.ComboChart(chartDiv);
      chart.draw(dataTable, chartOptions);

    }
    else if (dataJSON["type"] == "table") {
      // Making date table for chart
      let dataTable = new google.visualization.DataTable();
      // Adding columns
      for (let column of chartColumns) {
        dataTable.addColumn(column[0], column[1]);
      }
      // Adding rows
      dataTable.addRows(chartRows);
      let vMaxValue = dataTable.getColumnRange(1).max;
      vMaxValue += vMaxValue * .1;
      let table = new google.visualization.Table(chartDiv);
      table.draw(dataTable, { showRowNumber: true, width: '100%', height: '100%' });
    }
  }
}