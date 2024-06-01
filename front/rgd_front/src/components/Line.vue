<template>
    <div class="row height">
        <div class="col-sm-2">
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
            <div class="row">
                <div class="col stat_block left">
                    <div class="stat_block_up">Количество машин в структуре</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/graph.svg" alt="" width="100px" height="50px"></div>
                        <div class="stat_block_item">
                            <div class="text">{{ sum_car(Object.values(this.in_structure)) }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Количество машин не эксплуатируемых</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/graph.svg" alt="" width="100px" height="50px"></div>
                        <div class="stat_block_item">
                            <div class="text">{{ this.error_exploitation }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Нарушений в листах по датам</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/graph.svg" alt="" width="100px" height="50px"></div>
                        <div class="stat_block_item">
                            <div class="text">{{ this.error_date }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block right">
                    <div class="stat_block_up">Название</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/graph.svg" alt="" width="100px" height="50px"></div>
                        <div class="stat_block_item">
                            <div class="text">10 %</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-4 ">
                    <div class="division_block">
                        <div class="division_title">Эффективность регионов</div>
                        <div class="line"></div>
                        <div class="division_element">
                            <div class="image">
                                <img src="../assets/graph.svg" alt="" width="100px" height="50px">
                                <div class="regions">Приморье</div>
                            </div>
                            <div class="division_element_text">Эффертивность 10%</div>
                        </div>

                    </div>
                </div>
                <div class="col-8">
                    <div class="row graf_block">
                        <div class="col graf_block_left">
                            <div class="graf_block_title">График эффективности подразделений</div>
                            <div class="line"></div>
                            <div class="grafic">
                                <canvas id="myChart5"></canvas>
                            </div>
                        </div>
                        <div class="col graf_block_right">
                            <div class="graf_block_title">График количества нарушений подразделений</div>
                            <div class="line"></div>
                            <div class="grafic">
                                <canvas id="myChart6"></canvas>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <div class="row div_block">
                <div class="col row_margin_top">
                    <div class="row graf_block">
                        <div class="col">
                            <div class="graf_block_left">
                                <div class="graf_block_title">Анализ структурного подразделения с рекомендациями</div>
                                <div class="line"></div>
                                <div class="grafic">
                                    <canvas id="myChart4ы"></canvas>
                                </div>
                            </div>
                        </div>
                        <div class="col ">
                            <div class="graf_block_right">
                                <div class="graf_block_title">График количества нарушений подразделений</div>
                                <div class="line"></div>
                                <div class="grafic">
                                    <canvas id="myChart3"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>

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
                                backgroundColor: [
                                    'rgb(255, 99, 132)',
                                    'rgb(75, 192, 192)',
                                    'rgb(255, 205, 86)',
                                    'rgb(201, 203, 207)',
                                    'rgb(54, 162, 235)'
                                ]
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
                                backgroundColor: [
                                    'rgb(255, 99, 132)',
                                    'rgb(75, 192, 192)',
                                    'rgb(255, 205, 86)',
                                    'rgb(201, 203, 207)',
                                    'rgb(54, 162, 235)'
                                ]
                            }]

                        },

                    })
            }, 1000);

    },

}

</script>