<template>
    <div class="row">
        <div class="col-sm-2 height">
            <div class="item_list">
                <div class="list_title">
                    <div>Структурные подразделения</div>
                </div>
                <div class="list_messages" v-if="lines">
                    <div v-for="(line, index) in lines" :key='index'>
                        <div class="item" @click="Mark_get(line.id)">
                            <div>{{ line.name }}</div>
                            <img src="../assets/home.png" alt="" width="27px" height="27px">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-10 height">
            <div class="result">
                <div class="stat_title">Результат</div>
                <div class="stat_item">Количество машин в структуре - <b>{{ sum_car(Object.values(this.in_structure))
                        }}</b></div>
                <div>
                    <div v-for="(sub, index) in in_structure" :key='index'>
                        <div class="stat_item"><b>{{ index }}</b> - {{ sub }}</div>
                    </div>
                </div>

                <div class="stat_item">Количество машин не эксплуатируемых - <b>{{ this.error_exploitation }}</b></div>
                <div class="stat_item">Нарушений в дате - <b>{{ this.error_date }}</b></div>
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
                <div class="grafic">
                    <canvas id="myChart5"></canvas>
                </div>
                <div class="grafic">
                    <canvas id="myChart6"></canvas>
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
            lines: null,
            count: null,
            error_: null,
            not_error_: null,
            date: {

            },
            subdivisions: {},
            error_subdivisions: {},
            in_structure: {},
            error_mileage: null,
            error_date: null,
            error_exploitation: 0,
        }
    }, methods: {
        sum_car(arr) {
            let count = 0;
            for (let i = 0; i < arr.length; i++) {
                count += arr[i]
            }
            return count
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
            this.lines = response.data.subdivisions;
            for (let i = 0; i < response.data.subdivisions.length; i++) {
                this.subdivisions[response.data.subdivisions[i].name] = parseFloat(response.data.subdivisions[i].rating.substring(response.data.subdivisions[i].rating.length - 6, response.data.subdivisions[i].rating.length - 2));
                this.in_structure[response.data.subdivisions[i].name] = 0;
                if (!(response.data.subdivisions[i].name in this.error_subdivisions)) {

                    this.error_subdivisions[response.data.subdivisions[i].name] = 1;
                }
                for (let j = 0; j < response.data.subdivisions[i].vehicles.length; j++) {

                    if ((response.data.subdivisions[i].vehicles[j].all_telematics_mileage == response.data.subdivisions[i].vehicles[j].all_true_telematics_mileage) && (Number(response.data.subdivisions[i].vehicles[j].all_true_telematics_mileage) == 0)) {
                        this.error_exploitation += 1;
                    };

                    for (let k = 0; k < response.data.subdivisions[i].vehicles[j].trips.length; k++) {
                        if (response.data.subdivisions[i].vehicles[j].in_structure) {
                            this.in_structure[response.data.subdivisions[i].name] += 1;
                        };


                        if (response.data.subdivisions[i].vehicles[j].trips[k].trip_mileage == response.data.subdivisions[i].vehicles[j].trips[k].telematics_mileage) {
                            this.not_error_ += 1;

                        } else {
                            this.error_ += 1;
                            if (response.data.subdivisions[i].vehicles[j].trips[k].trip_date in this.date) {
                                console.log(1)
                                this.date[response.data.subdivisions[i].vehicles[j].trips[k].trip_date] += 1;
                                this.error_subdivisions[response.data.subdivisions[i].name] += 1;
                            } else {
                                if (!response.data.subdivisions[i].vehicles[j].trips[k].trip_date) {
                                    if (response.data.subdivisions[i].vehicles[j].trips[k].telematics_date) {
                                        if (response.data.subdivisions[i].vehicles[j].trips[k].telematics_date in this.date) {
                                            this.date[response.data.subdivisions[i].vehicles[j].trips[k].telematics_date] += 1;

                                        } else {
                                            this.date[response.data.subdivisions[i].vehicles[j].trips[k].telematics_date] = 1;
                                        }
                                    }

                                } else {
                                    this.date[response.data.subdivisions[i].vehicles[j].trips[k].trip_date] = 1;
                                }

                            }
                        };
                        if ((!response.data.subdivisions[i].vehicles[j].trips[k].trip_date) || (!response.data.subdivisions[i].vehicles[j].trips[k].telematics_date)) {
                            this.error_date += 1;

                        }

                    }
                }

            }


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

                    }),
                    new Chart(document.getElementById('myChart5'), {
                        type: 'polarArea',
                        data: {
                            labels: Object.keys(this.subdivisions),
                            datasets: [{
                                label: 'Качество в %',
                                data: Object.values(this.subdivisions),

                            }]

                        },

                    }),
                    new Chart(document.getElementById('myChart6'), {
                        type: 'polarArea',
                        data: {
                            labels: Object.keys(this.error_subdivisions),
                            datasets: [{
                                label: 'Количество нарушений',
                                data: Object.values(this.error_subdivisions),

                            }]

                        },

                    })
            }, 1000);

    },

}

</script>