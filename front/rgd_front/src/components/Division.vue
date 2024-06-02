<template>
    <div class="row height stat_page" v-if="drive_lvl">
        <div class="col-12 height">
            <div class="row">
                <div class="col stat_block left">
                    <div class="stat_block_up">Рейтинг подразделения</br></div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/raiting2.svg" alt=""></div>
                        <div class="stat_block_item stat_color_red">
                            <div class="text">{{ rating_subdivision }}%</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Количество машин</div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/car3.svg" alt=""></div>
                        <div class="stat_block_item stat_color_green">
                            <div class="text">{{ this.count_car }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block center">
                    <div class="stat_block_up">Износ транспорта</div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/engine.svg" alt=""></div>
                        <div class="stat_block_item stat_color_purple">
                            <div class="text">{{ this.wear_car.toFixed(2) }} Km</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block right">
                    <div class="stat_block_up">Качество вождения</div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/driving.svg" alt=""></div>
                        <div class="stat_block_item stat_color_blue">
                            <div class="text">{{ driving_styleType(drive_lvl) }}({{ drive_lvl.toFixed(1) }})</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block right">
                    <div class="stat_block_up">Транспорт в Стр подразделении</div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/buildings.svg" alt=""></div>
                        <div class="stat_block_item stat_color_orange">
                            <div class="text">{{ this.in_structure }} / {{ this.count_car }}</div>
                        </div>
                    </div>
                </div>
                <div class="col stat_block right">
                    <div class="stat_block_up">Неиспользуемый транспорт</div>
                    <div class="stat_block_down">
                        <div class="image icon"><img src="../assets/no_car.svg" alt=""></div>
                        <div class="stat_block_item stat_color_red">
                            <div class="text">{{ this.downtime_sr }}</div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="row">
                <div class="col-4 ">
                    <div class="division_block division_block_bottom2">
                        <div class="division_title">Список отчетов</div>
                        <div class="line"></div>
                        <div class="division_items">
                            <div class="division_element" v-for="(line, index) in lines" :key='index'
                                @click="Item_get(line.id)">
                                <div class="image">
                                    <img src="../assets/car_list.png" alt="" width="65px" height="65px">
                                    <div class="regions">Отчет - {{ line.number }}</div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <div class="col-8 ">
                    <div class="row graf_block division_block_bottom2">
                        <div class="col graf_block_left">
                            <div class="graf_block_title">График эффективности подразделений</div>
                            <div class="line"></div>
                            <div class="grafic">
                                <canvas id="myChart5"></canvas>
                            </div>
                        </div>
                        <div class="col graf_block_right right_element">
                            <div class="graf_block_title">График количества нарушений автотранспорта</div>
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
                        <div class="col-12">
                            <div class="division_block  division_block_bottom3">
                                <div class="division_title">Анализ структурного подразделения с рекомендациями</div>
                                <div class="line"></div>
                                <div class="division_items">
                                    <div class="division_element" @click="Item_get(line.id)">
                                        <div class="image">
                                            <img src="../assets/train2.svg" alt="" width="100px" height="50px">
                                            <div class="regions">{{ analis }}</div>
                                        </div>
                                    </div>
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
            count_car: null,
            wear_car: 0,
            drive_lvl: null,
            in_structure: null,
            downtime_sr: null,
            rating_subdivision: null,
            error_subdivisions: {},
            downtime_cars: {},
            analis: null,



            lines: null,
            is_ready: null,
        }
    }, methods: {
        sum_car(arr) {
            let count = 0;
            for (let i = 0; i < arr.length; i++) {
                count += arr[i]
            }
            return count
        },
        driving_styleType(ball) {
            if (ball < 2) {
                return "Критический";
            } else if (4 >= ball && ball > 2) {
                return "Средний"
            } else if (6 >= ball && ball > 4) {
                return "Хороший"
            }

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

        axios.get(this.$globalUrl + 'api/subdivision/' + this.route.params.division_id + "/").then(response => {
            this.rating_subdivision = parseFloat(response.data.rating.substring(response.data.rating.length - 7, response.data.rating.length - 2));
            let count = 0;
            this.analis = response.data.text_analysis;
            this.lines = response.data.vehicles;

            for (let i = 0; i < response.data.vehicles.length; i++) {
                this.count_car += 1;
                if (response.data.vehicles[i].all_true_telematics_mileage) {
                    console.log(parseFloat(response.data.vehicles[i].all_true_telematics_mileage));
                    this.wear_car += parseFloat(response.data.vehicles[i].all_true_telematics_mileage);


                    this.drive_lvl += parseFloat(response.data.vehicles[i].driving_style);

                    if (response.data.vehicles[i].all_true_telematics_mileage && parseInt(response.data.vehicles[i].all_true_telematics_mileage) == 0) {
                        this.downtime_sr += 1;
                    }
                    if (response.data.vehicles[i].in_structure) {
                        this.in_structure += 1;
                    }
                    if (!(response.data.vehicles[i].number in this.error_subdivisions)) {
                        this.error_subdivisions[response.data.vehicles[i].number] = 0;
                    }
                    this.downtime_cars[response.data.vehicles[i].number] = 0;

                    count++;
                }


                for (let j = 0; j < response.data.vehicles[i].trips.length; j++) {
                    if (response.data.vehicles[i].trips[j].trip_mileage != response.data.vehicles[i].trips[j].telematics_mileage) {
                        this.error_subdivisions[response.data.vehicles[i].number] += 1;

                    }
                    if (response.data.vehicles[i].trips[j].trip_date != response.data.vehicles[i].trips[j].telematics_date) {
                        this.error_subdivisions[response.data.vehicles[i].number] += 1;

                    }
                    if (response.data.vehicles[i].trips[j].telematics_mileage) {
                        this.downtime_cars[response.data.vehicles[i].number] += parseInt(response.data.vehicles[i].trips[j].telematics_mileage)
                    }



                }
            }
            this.wear_car = this.wear_car / count;
            this.drive_lvl = this.drive_lvl / count;
            console.log(count)
            console.log(this.wear_car)
        });




        setTimeout(() => {

            new Chart(document.getElementById('myChart5'), {
                type: 'bar',
                data: {
                    labels: Object.keys(this.downtime_cars),
                    datasets: [{
                        label: 'Километраж',
                        data: Object.values(this.downtime_cars),
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
                            label: 'Количество нарушений',
                            data: Object.values(this.error_subdivisions),
                            backgroundColor: [

                                'rgba(97, 94, 252, 0.8)',
                                'rgba(199, 56, 189, 0.8)',
                                'rgba(254, 122, 54, 0.8)',
                                'rgba(54, 82, 173, 0.8)',
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