<template>
    <div class="row">
        <div class="col-sm-2 height">
            <div class="item_list">
                <div class="list_title">
                    <div>Маршруты</div>
                </div>
                <div class="list_messages" v-if="lines">
                    <div v-for="(line, index) in lines" :key='index'>
                        <div class="item" @click="Mark_get(line.id)">
                            <div>{{ line.title }}</div>
                            <img src="../assets/home.png" alt="" width="27px" height="27px">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-10 height">
            <div class="result">
                <div class="stat_title">Результат</div>
                <div class="stat_item">Качество переговоров - <b>{{ this.sr_count }} %</b></div>
                <div class="stat_item">Качество нарушений - <b>{{ this.count_not_accept }}</b></div>
                <div class="stat_item">Качество переговоров без нарушений - <b>{{ this.count_accept }}</b></div>
                <div class="grafic">
                    <canvas id="myChart"></canvas>
                </div>
                <div class="grafic">
                    <canvas id="myChart2"></canvas>
                </div>
                <div class="grafic">
                    <canvas id="myChart3"></canvas>
                </div>
                <div class="grafic">
                    <canvas id="myChart4"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import axios from 'axios';
import Chart from 'chart.js/auto';
export default {
    data() {
        return {
            count: null,
            error_: null,
            not_error_: null,
            date: {

            }
        }
    },
    setup() {
        const router = useRouter();
        const route = useRoute();
        function Mark_get(id) {
            router.push('/route/' + id);
        };
        function Item_get(id) {
            router.push('/route/' + route.params.category_id + '/chat/' + id);
        };
        return {
            Mark_get, Item_get, route
        }
    },
    mounted() {
        axios.get(this.$globalUrl + 'api/regions/' + this.route.params.category_id + "/").then(response => {
            this.dialog = response.data;
            for (let i = 0; i < response.data.subdivisions.length; i++) {
                for (let j = 0; j < response.data.subdivisions[i].vehicles.length; j++) {
                    for (let k = 0; k < response.data.subdivisions[i].vehicles[j].trips.length; k++) {
                        if (response.data.subdivisions[i].vehicles[j].trips[k].trip_mileage == response.data.subdivisions[i].vehicles[j].trips[k].telematics_mileage) {
                            this.not_error_ += 1;

                        } else {
                            this.error_ += 1;
                            if (response.data.subdivisions[i].vehicles[j].trips[k].trip_date in this.date) {
                                let s =
                                    this.date[response.data.subdivisions[i].vehicles[j].trips[k].trip_date] += 1;
                            } else {
                                console.log(response.data.subdivisions[i].vehicles[j].trips[k].trip_date)
                                this.date[response.data.subdivisions[i].vehicles[j].trips[k].trip_date] = 1;
                            }
                        }



                    }
                }

            }
            console.log(Object.keys(this.date), Object.values(this.date))

        }),

            setTimeout(() => {

                new Chart(document.getElementById('myChart'), {
                    type: 'pie',
                    data: {
                        labels: ["Нарушения", "Без нарушений"],
                        datasets: [{
                            label: "Единиц",
                            backgroundColor: ["#FF3300", "#339966"],
                            data: [this.error_, this.not_error_]
                        }]
                    },
                    options: {
                        title: {
                            display: true,
                            text: 'Predicted world population (millions) in 2050'
                        },
                        responsive: true,

                    }
                }),
                    new Chart(document.getElementById('myChart2'), {
                        type: 'radar',
                        data: {
                            labels: [
                                'Eating',
                                'Drinking',
                                'Drinkin2g',
                            ],
                            datasets: [{
                                label: 'My First Dataset',
                                data: [65, 59, 90],
                                fill: true,
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                borderColor: 'rgb(255, 99, 132)',
                                pointBackgroundColor: 'rgb(255, 99, 132)',
                                pointBorderColor: '#fff',
                                pointHoverBackgroundColor: '#fff',
                                pointHoverBorderColor: 'rgb(255, 99, 132)'
                            }, {
                                label: 'My Second Dataset',
                                data: [28, 48, 40],
                                fill: true,
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgb(54, 162, 235)',
                                pointBackgroundColor: 'rgb(54, 162, 235)',
                                pointBorderColor: '#fff',
                                pointHoverBackgroundColor: '#fff',
                                pointHoverBorderColor: 'rgb(54, 162, 235)'
                            }]

                        },
                        options: {
                            title: {
                                display: true,
                                text: 'Predicted world population (millions) in 2050'
                            },
                            responsive: true,

                        }
                    }),
                    new Chart(document.getElementById('myChart3'), {
                        type: 'line',
                        data: {
                            labels: Object.keys(this.date),
                            datasets: [{
                                label: 'My First Dataset',
                                data: Object.values(this.date),
                                fill: false,
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            }]

                        },

                    }),
                    new Chart(document.getElementById('myChart4'), {
                        type: 'scatter',
                        data: {
                            labels: Object.keys(this.date),
                            datasets: [{
                                type: 'bar',
                                label: 'Bar Dataset',
                                data: Object.values(this.date),
                                borderColor: 'rgb(255, 99, 132)',
                                backgroundColor: 'rgba(255, 99, 132, 0.2)'
                            }]

                        },

                    })
            }, 1000);

    },

}

</script>