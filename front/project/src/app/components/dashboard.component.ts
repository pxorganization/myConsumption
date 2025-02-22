import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Chart } from 'chart.js/auto';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="chart-container">
      <div class="card">
        <h3>Daily Prices</h3>
        <canvas id="priceChart"></canvas>
      </div>

      <div class="card">
        <h3>Energy Consumption</h3>
        <canvas id="usageChart"></canvas>
      </div>
    
      <div class="card">
        <h3>Energy Cost</h3>
        <canvas id="costChart"></canvas>
      </div>
    </div>
  `
})
export class DashboardComponent implements OnInit {
  ngOnInit() {
    this.createPriceChart();
    this.createUsageChart();
    this.createCostChart();
  }

  createPriceChart() {
    const ctx = document.getElementById('priceChart') as HTMLCanvasElement;
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: [107.09, 104, 100, 85.66, 85, 85.53, 95.07, 103.07, 65, 47.34, 1, 0.54, 2.24, 3.24, 65.1, 96.1, 14, 23, 21, 12, 19, 12, 19, 15],
          backgroundColor: '#00A3E0',
          borderRadius: 5
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        responsive: true,
        scales: { 
          y: {
             beginAtZero: true,
             title: {
              display: true,
              text: 'Price (€/kWh)',
              font: {
                size: 14,
                weight: 'normal'
              }
             } 
            }, 
          x: {
            title: {
              display: true,
              text: 'Time (Hours)', 
              font: {
                size: 14,
                weight: 'normal'
              }
            }
          }
        }
      }
    });
  }



  createUsageChart() {
    const ctx = document.getElementById('usageChart') as HTMLCanvasElement;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: [90, 120, 180, 150, 100, 160, 140, 130, 110, 100, 90, 120, 180, 150, 100, 160, 140, 130, 110, 100, 100, 160, 140, 130],
          borderColor: '#005F8C',
          fill: true,
          backgroundColor: 'rgba(0, 96, 140, 0.34)',
          tension: 0.4
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { 
          y: {
             beginAtZero: true,
             title: {
              display: true,
              text: 'Consumption (kWh)',
              font: {
                size: 14,
                weight: 'normal'
              }
             } 
            }, 
          x: {
            title: {
              display: true,
              text: 'Time (Hours)', 
              font: {
                size: 14,
                weight: 'normal'
              }
            }
          }
        }
      }
    });
  }

  createCostChart() {
    const ctx = document.getElementById('costChart') as HTMLCanvasElement;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: [90, 120, 180, 150, 100, 160, 140, 130, 110, 100, 90, 120, 180, 150, 100, 160, 140, 130, 110, 100, 100, 160, 140, 130],
          borderColor: '#fa4616',
          fill: true,
          backgroundColor: 'rgba(250, 71, 22, 0.36)',
          tension: 0.4
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { 
          y: {
             beginAtZero: true,
             title: {
              display: true,
              text: 'Cost (€)',
              font: {
                size: 14,
                weight: 'normal'
              }
             } 
            }, 
          x: {
            title: {
              display: true,
              text: 'Time (Hours)', 
              font: {
                size: 14,
                weight: 'normal'
              }
            }
          }
        }
      }
    });
  }

  // createDeviceScheduleChart() {
  //   const canvas = document.getElementById('deviceChart') as HTMLCanvasElement;
  //   const ctx = canvas.getContext('2d');
  //   if (!ctx) {
  //     console.error('Failed to get 2D context');
  //     return;
  //   }

  //   new Chart(ctx, {
  //     type: 'bar',
  //     data: {
  //       labels: ['Dish washer', 'Oven'], // Devices
  //       datasets: [
  //         {
  //           label: 'Operating Window',
  //           data: [
  //             { x: 6, x2: 18, y: 0 }, // Dishwasher
  //             { x: 5, x2: 19, y: 1 }  // Oven
  //           ],
  //           backgroundColor: '#00A3E0'
  //         },
  
  //         // 🔹 Assigned Period (Drawn on top)
  //         {
  //           label: 'Assigned Timeslot',
  //           data: [
  //             { x: 12, x2: 14, y: 0 }, // Dishwasher
  //             { x: 17, x2: 18, y: 1 }  // Oven
  //           ],
  //           backgroundColor: '#ffa200'
  //         }
  //       ]
  //     },
  //     options: {
  //       indexAxis: 'y', // Make the chart horizontal
  //       scales: {
  //         x: {
  //           type: 'linear',
  //           position: 'bottom',
  //           min: 0,
  //           max: 23, 
  //           ticks: {
  //             stepSize: 1
  //           },
  //           title: {
  //             display: true,
  //             text: 'Time (Hours)',
  //             font: {
  //               size: 14,
  //               weight: 'normal'
  //             }
  //           }
  //         },
  //         y: {
  //           title: {
  //             display: false,
  //             text: 'Devices',
  //             font: {
  //               size: 14,
  //               weight: 'normal'
  //             }
  //           }
  //         }
  //       }
  //     }
  //   });
  // }
}