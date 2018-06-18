var zones = []
var currentZone
var zoneTempLineChart, zonePHLineChart, zoneCO2LineChart,moduleTempLineChart, moduleGroundHumidityLineChart,
 moduleEnvHumidityLineChart, moduleWaterBarChart,moduleCO2BarChart,plantEnvHumidityLineChart

var type_selected_obj
var id_selected_obj

$(document).ready(function (){
  let id_selected_zone = $('#zona').val()
  type_selected_obj = 'zona'
  id_selected_obj = id_selected_zone
  setCharts()
  checkStatsZone(id_selected_zone)
})

function changeZone(){
  let id_selected_zone = $('#zona').val()
  type_selected_obj = 'zona'
  id_selected_obj = id_selected_zone
  $('#moduleCharts').hide()
  $('#plantCharts').hide()
  checkStatsZone(id_selected_zone)
}

function changeModule(){
  let id_selected_module = $('#comboModule').val()
  if (id_selected_module == 'all'){
    changeZone()
  } else {
    $('#zoneCharts').hide()
    $('#plantCharts').hide()
    type_selected_obj = 'modulo'
    id_selected_obj = id_selected_module
    checkStatsModule(id_selected_module)
  }
}

function changePlant(){
  let id_selected_plant = $('#comboPlant').val()
  if (id_selected_plant == 'all'){
    changeZone()
  } else {
    $('#zoneCharts').hide()
    $('#moduleCharts').hide()
    type_selected_obj = 'planta'
    id_selected_obj = id_selected_plant
    checkStatsPlants(id_selected_plant)
  }
}

function checkStatsModule(id_module){
  let module
  for (let i = 0; i < currentZone['modules'].length; i++) {
    if (currentZone.modules[i].idmodulo == id_module) {
      module = currentZone.modules[i]
      break
    }
  } 
  moduleTempLineChart.data.labels = module.fecharegistro
  moduleTempLineChart.data.datasets[0].data = module.temperatura
  moduleTempLineChart.update()
  moduleGroundHumidityLineChart.data.labels = module.fecharegistro
  moduleGroundHumidityLineChart.data.datasets[0].data = module.humedadtierra
  moduleGroundHumidityLineChart.update()
  moduleEnvHumidityLineChart.data.labels = module.fecharegistro
  moduleEnvHumidityLineChart.data.datasets[0].data = module.humedadambiente
  moduleEnvHumidityLineChart.update()
  moduleWaterBarChart.data.labels = module.fecharegistro
  moduleWaterBarChart.data.datasets[0].data = module.nivelagua
  moduleWaterBarChart.update()
  moduleCO2BarChart.data.labels = module.fecharegistro
  moduleCO2BarChart.data.datasets[0].data = module.concentracionco2
  moduleCO2BarChart.update()
  $('#moduleCharts').show()
}


function setCharts(){
  commonLineData = {
    labels: [],
    datasets: [
      {
        label: "",
        //backEnvColor: "rgba(38, 185, 154, 0.31)",
        borderColor: "rgba(38, 185, 154, 0.7)",
        pointBorderColor: "rgba(38, 185, 154, 0.7)",
        pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(220,220,220,1)",
        pointBorderWidth: 1,
        lineTension: 0,
        data: []
      }
    ]
  }
  commonLineOptions = {
    type: 'line',
    data: commonLineData,
    maintainAspectRatio: false,
    options: {
      scales: {
        yAxes: [{
          ticks: { 
            beginAtZero: true
          }
        }]
      }
    }
  }
  commonBarData = {
    labels: [],
    datasets: [
      {
        label: "",
        backgroundColor: "rgba(115, 135, 156, 0.8)",
        pointBorderWidth: 1,
        data: []
      }
    ]    
  }
  commonBarOptions = {
    type: 'bar',
    data: commonBarData,
    options: {
      scales: {
        yAxes: [{
          ticks: { 
            beginAtZero: true
          }
        }]
      }
    }
  } 

  let ctx = document.getElementById("zoneTempLineChart")
  zoneTempLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("zonePHLineChart")
  zonePHLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("zoneCO2LineChart")
  zoneCO2LineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("moduleTempLineChart")
  moduleTempLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("moduleGroundHumidityLineChart")
  moduleGroundHumidityLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("moduleEnvHumidityLineChart")
  moduleEnvHumidityLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
  ctx = document.getElementById("moduleWaterBarChart")
  moduleWaterBarChart = new Chart(ctx, JSON.parse(JSON.stringify(commonBarOptions)));
  ctx = document.getElementById("moduleCO2BarChart")
  moduleCO2BarChart = new Chart(ctx, JSON.parse(JSON.stringify(commonBarOptions)));
  ctx = document.getElementById("plantEnvHumidityLineChart")
  plantEnvHumidityLineChart = new Chart(ctx, JSON.parse(JSON.stringify(commonLineOptions)));
}

function checkStatsZone(id_zone){
  if (zones[id_zone]){
    updateChildSelects(id_zone)
    viewZoneStats(id_zone)
  } else {        
    getZoneInformation(id_zone)
  }
}

function getZoneInformation(id_zone){
  url = '../api/stats/zone/'
  data = {
    'idzona': id_zone
  }
  $.getJSON(url, data=data, function(result){
    zones[id_zone] = result
  })
  .then(() => {
    updateChildSelects(id_zone)
    viewZoneStats(id_zone)
    }    
  )
}

function viewZoneStats(id_zone){
  currentZone = zones[id_zone]
  zoneTempLineChart.data.labels = currentZone['fecharegistro']
  zoneTempLineChart.data.datasets[0].data = currentZone['temperatura']
  zoneTempLineChart.update()
  zonePHLineChart.data.labels = currentZone['fecharegistro']
  zonePHLineChart.data.datasets[0].data = currentZone['ph']
  zonePHLineChart.update()
  zoneCO2LineChart.data.labels = currentZone['fecharegistro']
  zoneCO2LineChart.data.datasets[0].data = currentZone['concentracionco2']
  zoneCO2LineChart.update()
  $('#zoneCharts').show()
}

function updateChildSelects(id_zone){
  currentZone = zones[id_zone]
  if (currentZone['idtipozona'] == 1){
    $('#divComboModules').show()
    $('#divComboPlants').hide()

    $('#comboModule').empty()
    $('#comboModule')
      .append($('<option>', {
        value: 'all',
        text: '-'
      }))
    let modules = currentZone['modules']
    for (let i = 0; i < modules.length; i++){
      let module = modules[i]
      $('#comboModule')
        .append($('<option>', {
          value: module['idmodulo'],
          text: module['nombre']
        }))
    }
  } else if (currentZone['idtipozona'] == 2) {
    $('#divComboModules').hide()
    $('#divComboPlants').show()

    $('#comboPlant').empty()
    $('#comboPlant')
      .append($('<option>', {
        value: 'all',
        text: '-'
      }))
    let plants = currentZone['plants']
    for (let i = 0; i < plants.length; i++){
      let plant = plants[i]
      $('#comboPlant')
        .append($('<option>', {
          value: plant['idplanta'],
          text: plant['nombrecomun']
        }))
    }
  }
}

function checkStatsPlants(id_plant){
  let plant
  for (let i = 0; i < currentZone['plants'].length; i++) {
    if (currentZone.plants[i].idplanta == id_plant) {
      plant = currentZone.plants[i]
      break
    }
  }
  plantEnvHumidityLineChart.data.labels = plant.fecharegistro
  plantEnvHumidityLineChart.data.datasets[0].data = plant.humedad
  plantEnvHumidityLineChart.update()
  $('#plantCharts').show()
}