<template>
    <div class="row height stat_page" v-if="error_subdivisions">
        <div class="col-12 height">
            <div class="row">
                <div class="col stat_block left">
                    <div class="stat_block_up">Количество машин в структуре</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/car_2.svg" alt="" width="100px" height="100px"></div>
                        <div class="stat_block_item stat_color_green">
                            <div class="text">{{ sum_car(Object.values(this.in_structure)) }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Количество машин не эксплуатируемых</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/car_1.svg" alt="" width="100px" height="100px"></div>
                        <div class="stat_block_item stat_color_blue">
                            <div class="text">{{ this.error_exploitation }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Нарушений в листах по датам</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/calendar.svg" alt="" width="100px" height="100px"></div>
                        <div class="stat_block_item stat_color_red">
                            <div class="text">{{ this.error_date }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block right">
                    <div class="stat_block_up">Общий рейтинг управления ЖД</div>
                    <div class="stat_block_down">
                        <div class="image"><img src="../assets/raiting2.svg" alt="" width="100px" height="100px"></div>
                        <div class="stat_block_item stat_color_orange">
                            <div class="text">68 %</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-4 ">
                    <div class="division_block">
                        <div class="division_title">Эффективность подразделений</div>
                        <div class="line"></div>

                        <div class="division_element" v-for="(line, index) in lines" :key='index'
                            @click="Item_get(line.id)">
                            <div class="image">
                                <img src="../assets/train.svg" alt="" width="100px" height="50px">
                                <div class="regions">{{ line.name }}</div>
                            </div>
                            <div class="division_element_text">Эффертивность {{ line.rating.substring(line.rating.length
                                - 7, line.rating.length - 2) }}%</div>
                        </div>

                    </div>
                </div>
                <div class="col-8 ">
                    <div class="row graf_block ">
                        <div class="col graf_block_left">
                            <div class="graf_block_title">График эффективности подразделений</div>
                            <div class="line"></div>
                            <div class="grafic">
                                <canvas id="myChart5"></canvas>
                            </div>
                        </div>
                        <div class="col graf_block_right right_element">
                            <div class="graf_block_title">График количества нарушений подразделений</div>
                            <div class="line"></div>
                            <div class="grafic">
                                <canvas id="myChart6"></canvas>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <div class="row">
                <div class="col-12 row_margin_top right_col row_margin_bottom">
                    <div class="row">
                        <div class="col-6">
                            <div class="division_block  division_block_bottom">
                                <div class="division_title">Анализ структурного подразделения с рекомендациями</div>
                                <div class="line"></div>
                                <div class="division_items">
                                    <div class="division_element" v-for="(line, index) in lines" :key='index'
                                        @click="Item_get(line.id)">
                                        <div class="image">
                                            <img src="../assets/train2.svg" alt="" width="100px" height="50px">
                                            <div class="regions">{{ line.name }} - {{ line.text_analysis }}</div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                        <div class="col-6">
                            <div class="graf_block_right division_block_bottom">
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
    <div class="search" v-else>
        <img src="../assets/search_train.gif" alt="" width="60%" height="60%">
        <div class="search_text">Загрузка данных</div>
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
            is_ready: null,
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
        function Item_get(id) {
            router.push('/region/' + route.params.category_id + '/division/' + id);
        };
        return {
            Item_get, route
        }
    },
    mounted() {
        axios.get(this.$globalUrl + 'api/regions/' + this.route.params.category_id + "/").then(response => {
            this.dialog = response.data;
            this.lines = response.data.subdivisions;
            for (let i = 0; i < response.data.subdivisions.length; i++) {
                this.subdivisions[response.data.subdivisions[i].name] = parseFloat(response.data.subdivisions[i].rating.substring(response.data.subdivisions[i].rating.length - 7, response.data.subdivisions[i].rating.length - 2));
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
                            label: 'Количество несоотвествий / Дата',
                            data: Object.values(this.date),
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]

                    },
                }),
                    new Chart(document.getElementById('myChart5'), {
                        type: 'bar',
                        data: {
                            labels: Object.keys(this.subdivisions),
                            datasets: [{
                                label: 'Структурные подразделения',
                                data: Object.values(this.subdivisions),
                                backgroundColor: [
                                    'rgba(97, 94, 252, 0.8)',
                                    'rgba(199, 56, 189, 0.8)',
                                    'rgba(254, 122, 54, 0.8)',
                                    'rgba(54, 82, 173, 0.8)',
                                ],

                                borderWidth: 3
                            }]
                        },

                    }),
                    new Chart(document.getElementById('myChart6'), {
                        type: 'bar',
                        data: {
                            labels: Object.keys(this.error_subdivisions),
                            datasets: [{
                                label: 'Структурные подразделения',
                                data: Object.values(this.error_subdivisions),
                                backgroundColor: [

                                    'rgba(97, 94, 252, 0.8)',
                                    'rgba(199, 56, 189, 0.8)',
                                    'rgba(254, 122, 54, 0.8)',
                                    'rgba(54, 82, 173, 0.8)',
                                    'rgba(54, 162, 235, 0.2)',
                                    'rgba(153, 102, 255, 0.2)',
                                    'rgba(201, 203, 207, 0.2)'
                                ],

                                borderWidth: 3
                            }]
                        },

                    })

            }, 1000);
        this.is_ready = true;

    },

}

</script>