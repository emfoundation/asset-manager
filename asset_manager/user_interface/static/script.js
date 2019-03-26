//API Call
axios.get('http://circulareconomy.space/api/assets')
  .then(function (response) {
    //const data = JSON.stringify(response.data, null, 4);
    const data = response.data;
    const dataContainer = document.querySelector('#data-container');
    //console.log(data);
    //dataContainer.innerHTML = data[0].id;
    //dataContainer.innerHTML = typeof data;

    chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true,
          }
        }]
      }
    };

    $("#loadGraph").click(
      function(){
      form = document.getElementById("graphSelector")
      //dataType
      if (form.dataType.value == "owner") {
        ////console.log("owner");
        labels = []
        chartData = []
        for(i=0;i<data.length;i++){
          if(labels.includes(data[i].owner)){ chartData[labels.indexOf(data[i].owner)]++; }
          else {
            chartData.push(1);
            labels.push(data[i].owner);
          }
        }
      } else if (form.dataType.value == "format") {
        //console.log("format");
        labels = []
        chartData = []
        for(i=0;i<data.length;i++){
          if(labels.includes(data[i].format)){ chartData[labels.indexOf(data[i].format)]++; }
          else {
            chartData.push(1);
            labels.push(data[i].format);
          }
        }
      } else if (form.dataType.value == "filetype") {
        //console.log("filetype");
        labels = []
        chartData = []
        for(i=0;i<data.length;i++){
          currentFile = data[i].filetype
          if(currentFile == "") {currentFile = "other"}
          if(labels.includes(currentFile)){ chartData[labels.indexOf(currentFile)]++; }
          else {
            chartData.push(1);
            labels.push(currentFile);
          }
        }
      } else if(form.dataType.value == "tag") {
        //console.log("tag");
        labels = []
        chartData = []
        for(i=0;i<data.length;i++){
          for(j=0;j<data[i].tags.length;j++){
            if(labels.includes(data[i].tags[j])){ chartData[labels.indexOf(data[i].tags[j])]++; }
            else {
              chartData.push(1);
              labels.push(data[i].tags[j]);
            }
          }
        }
      }

      //drawChart
      var ctx = document.getElementById("chart").getContext('2d');
      var myChart = new Chart(ctx,{
        type: form.chartType.value,
        data: {
          labels: labels,
          datasets: [{
            label: 'Chart Label',
            backgroundColor: 'rgb(255,0,0)',
            fill: false,
            data: chartData,
          }],
        },
        options: chartOptions
      })
  });


    //end
    const loadingMessage = document.querySelector('.loading-message');
    loadingMessage.classList.remove('is-visible');
  })
  .catch(function (error) {
    console.log(error);
  })
