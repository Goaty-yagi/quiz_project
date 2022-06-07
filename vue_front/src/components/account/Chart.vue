<template>
    
        <Radar
        :chart-options="chartOptions"
        :chart-id="chartId"
        :dataset-id-key="datasetIdKey"
        :plugins="plugins"
        :css-classes="cssClasses"
        :styles="styles"
        :width="width"
        :height="height"
        />
    
</template>

<script>
import { Radar } from 'vue-chartjs'
import Chart from 'chart.js/auto';
import { Chart as 
    ChartJS, 
    Title, 
    Tooltip, 
    Legend, 
    PointElement,
    RadialLinearScale,
    LineElement,
    Plugin } from 'chart.js'

import ChartDataLabels from 'chartjs-plugin-datalabels';
ChartJS.register(Title, Tooltip, Legend, PointElement, RadialLinearScale, LineElement, ChartDataLabels)

export default {
    name: 'Chart',
    components: { Radar },
    props: {
        chartdata: {
            type: Object,
            default: null
            },
        chartId: {
            type: String,
            default: ''
        },
        datasetIdKey: {
            type: String,
            default: 'label'
        },
        width: {
            type: Number,
            default: 375
        },
        height: {
            type: Number,
            default: 400
        },
        cssClasses: {
            default: '',
            type: String
        },
        styles: {
            type: Object,
            default: () => []
        },
        plugins: {
            type: Array,
            default: () => []
        }
    },
    data() {
        Chart.defaults.color = '#fff'
        Chart.defaults.plugins.title.display = false
        return {
            // width should be modify laler
            
            
            // chartData: {
            //     labels: [ 'ひらがな', 'カタカナ', 'ボキャブラリー', 'すうじ' ],
            //     datasets: [{ 
            //         label: "超初級正解率",
            //         // data: [10, 9, 8.3, 7],
            //         borderWidth:1,
            //         //   fill: true,
            //         //   borderDash: [9],
            //         //   borderDashOffset: 0.9,
            //         //   clip: 'object',
            //         //   order:1,
            //         //   tension:1,
            //         //   spanGaps: true,
            //         //   borderJoinStyle: 'bevel',
            //         //   pointRotation:90,
            //         backgroundColor: 'rgba(255, 153, 51, 0.2)',
            //         borderColor: ' #ff9933',
            //         pointBackgroundColor: 'rgb(255, 99, 132)',
            //         pointBorderColor: '#fff',
            //         pointHoverBackgroundColor: '#fff',
            //         pointHoverBorderColor: 'red'
            //     }],
            // },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    datalabels: {
                        display: false
                    },
                    legend: { display: false
                    },
                },
                scales:{
                    r:{
                        beginAtZero: true,
                        min:0,
                        max:10,
                        grid: {
                            color: "gray",
                        },
                        angleLines: {
                            color: 'white',
                        },
                        ticks: {
                            maxTicksLimit: 3,
                            display: false
                        },
                    }
                },        
            }
        }
    },
    mounted(){
        // Chart.defaults.plugins.title.display = false
        // Chart.defaults.plugins = false
        
        // Chart.defaults.font.size = 16
            // let a = document.getElementsByTagName('canvas')
            console.log(Chart.defaults)
            // a.setAttribute('style','padding:1rem')
        
        

    }
}
</script>
<style scoped lang="scss">
// canvas{
//     padding: 20rem;
// }
// .chart-container{
    
// }

</style>