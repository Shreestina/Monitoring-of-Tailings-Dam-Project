// Assigne URL variable to JSON data
url_nodes = "/api/v1.0/nodes"
url_node_id = "/api/v1.0/Node_id/"
url_sample = "/api/v1.0/sample/"

// Define optionChange function being called in HTML file
function optionChanged(subject) {
    buildPlots(subject);
}

     
// Populate Node_ids on drop down

// Define json data as variable
var node_dd = d3.json(url_nodes)

// Console log to see if data is accessible
node_dd.then(function(data) {
    console.log(data)
});



// Define init function
//function init() {
   
    var selector = d3.select('#selDataset');
    // Populate dropdown list with subject id's
    d3.json(url_nodes).then((data) => {
        console.log(data)
        data.forEach(value => {
         selector
            .append('option')
            .text(value)
            .property('value');
        }
        );

        buildPlots(data[0])
    });
  
    

// Functon for Building Plots 
function buildPlots(selection) {
    d3.json(url_node_id + selection).then((data) => {
        console.log(data)
       

        // Call buildGauge function with Latest_pressure data
        buildGauge(data.Latest_pressure,data.Node_id,data.Date_last_reading);

        // Filled piezometer information table data 
        var demoBox = d3.select('#sample-metadata');
        demoBox.html('');
        Object.entries(data).forEach(function([key, value],index){
            console.log(`${key}: ${value}`)
            if(index<=10) {

            demoBox.append('p').text(`${key}: ${value}`);
            }});
           

       
        // Populate Horizontal Bar Chart 
        var barChart = d3.select('#bar');
        barChart.html('');
        
        var sampleValues = [data.Maxpressure,data.Minimumpressure];
        var otuIDs = ["<b>Max</b><br>Pressure", "<b>Min</b><br>Pressure"];
        var otuLabels = ["Maximum Pore Water Pressure in VWP"+''+data.Node_id, "Minimum Pore Water Pressure in VWP"+''+data.Node_id];
        var hbData = [{
            type: 'bar',
            x: sampleValues.slice(0,2).reverse(),
            y: otuIDs.map(otu => 'VWP' + ' ' + otu).slice(0,2).reverse(),
            text: otuLabels.slice(0,2).reverse(),
            orientation: 'h',
           }];
           var layout = {
            title: '<b>Max and Min Historical PWP Values</b><br>(VWP'+" "+data.Node_id+" "+'in kPa)',
            barmode: 'stack',
            xaxis: { title: "Pressure(kPa)"},
           
            };
         

        Plotly.newPlot('bar', hbData, layout);
        
        d3.json(url_sample + selection).then((data2) => {
            console.log(data2)

        // Building Scatter Chart 
        var scatterChart = d3.select('#scatter');
        scatterChart.html('');
        var trace1 = {
            x: data2.Sample_date, //Dates
            y: data2.sample_values, //Pressure(kPa)
            text: "Pore water pressure reading in VWP"+" "+data.Node_id +" "+ "at"+" "+ "Y3 Paddock",
            mode: 'lines+markers',
            type:'scatter',
            marker: {
                color: otuIDs,
                size: sampleValues,
                colorscale: 'Earth',
            }
        };

        var bbData = [trace1];

        var layout ={
            title: " Trend of Water Pressure in VWP "+data.Node_id,
            //xaxis: { title: "Date"},
            yaxis: { title: "Pressure(kPa)"}
      
          };
        Plotly.newPlot('scatter', bbData, layout);

  
    });
})}