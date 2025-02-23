import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Chart } from 'chart.js/auto';
import { ApiService } from '../services/api.service'; // Adjust the path based on your project structure
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="chart-wrapper">
      <div class="chart-grid">
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


        <div class="card">
        <div class="card" style="background: linear-gradient(45deg, rgb(0, 82, 212), rgb(67, 100, 247), rgb(111, 177, 252));" >
          <h3>Comparison Plan 1 </h3>
          <div class="comparison-value">{{ comparisonData[0] }}</div>
        </div>
        <div class="card" style="background: linear-gradient(45deg, rgb(17, 153, 142), rgb(56, 239, 125));">
          <h3>Comparison Plan 2</h3>
          <div class="comparison-value"><i class="fas fa-arrow-down"></i>{{ comparisonData[1] }}</div>
        </div>
        <div class="card" style="background: linear-gradient(45deg, rgb(255, 195, 18), rgb(247, 240, 31));"
        >
          <h3>Comparison Plan 3</h3>
          <div class="comparison-value">{{ comparisonData[2] }}</div>
        </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chart-wrapper {
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 20px;
      max-width: 1200px; /* Limit maximum width for large screens */
      margin: 0 auto; /* Center the wrapper horizontally */
    }
  
    .chart-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* Προσαρμόζεται δυναμικά */
      gap: 20px;
      width: 100%;
    }
  
    .card {
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      min-width: 0; /* Prevents overflow */
      max-width: 100%; /* Ensures cards don’t exceed container width */
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
  
    h3 {
      margin: 0 0 20px 0;
      font-size: 18px;
      font-weight: 600;
    }
  
    canvas {
      width: 100% !important;
      height: 300px !important; /* Default height for larger screens */
      max-height: 300px; /* Prevents excessive growth */
    }
  
    .comparison-value {
      font-size: 24px;
      font-weight: bold;
      color: #333;
    }
  
    /* Position the charts in the grid */
    .card:nth-child(1) { grid-column: 1; grid-row: 1; } /* Daily Prices (top left) */
    .card:nth-child(2) { grid-column: 2; grid-row: 1; } /* Energy Consumption (top right) */
    .card:nth-child(3) { grid-column: 1; grid-row: 2; } /* Energy Cost (bottom left) */
    .card:nth-child(4) { grid-column: 2; grid-row: 2; } /* Comparison Plan 1 (bottom right) */
    .card:nth-child(5) { grid-column: 1; grid-row: 3; } /* Comparison Plan 2 (bottom left) */
    .card:nth-child(6) { grid-column: 2; grid-row: 3; } /* Comparison Plan 3 (bottom right) */
  
    /* Large screens (desktops, > 1200px) */
    @media (min-width: 1200px) {
      .chart-grid {
        grid-template-columns: repeat(2, 1fr); /* Maintain two columns */
        grid-template-rows: repeat(3, 1fr); /* Maintain three rows */
      }
      canvas {
        height: 300px !important; /* Keep default height */
      }
    }
  
    /* Medium screens (tablets, 768px - 1200px) */
    @media (min-width: 768px) and (max-width: 1199px) {
      .chart-grid {
        grid-template-columns: repeat(2, 1fr); /* Maintain two columns */
        grid-template-rows: repeat(3, 1fr); /* Maintain three rows */
      }
      canvas {
        height: 250px !important; /* Reduce height for better fit on tablets */
      }
    }
  
    /* Small screens (tablets and below, ≤ 767px) */
    @media (max-width: 767px) {
      .chart-grid {
        display: flex;
        flex-direction: column;
        gap: 20px;
        grid-template-columns: 1fr; /* Μία στήλη */
        grid-template-rows: auto; 
      }
      .card {
        grid-column: auto; /* Reset column span for stacking */
        grid-row: auto; /* Reset row span for stacking */
      }
      canvas {
        height: 220px !important; /* Reduce height for smaller screens to ensure readability */
      }
    }
  
    /* Very small screens (mobile, ≤ 480px) */
    @media (max-width: 480px) {
      .chart-grid {
        grid-template-columns: 1fr; /* Ensure single column on mobile */
      }
      .card {
        grid-column: auto; /* Reset column span for stacking */
        grid-row: auto; /* Reset row span for stacking */
      }
      canvas {
        height: 180px !important; /* Further reduce height on mobile for better fit */
      }
      h3 {
        font-size: 16px; /* Slightly reduce heading size on very small screens */
      }
    }
  
    /* Extra-large screens (adjust if needed) */
    @media (min-width: 1400px) {
      .chart-grid {
        grid-template-columns: repeat(2, 1fr); /* Maintain two columns */
        grid-template-rows: repeat(3, 1fr); /* Maintain three rows */
      }
      canvas {
        height: 350px !important; /* Slightly increase height for very large screens */
      }
    }
  `]
})
export class DashboardComponent implements OnInit, AfterViewInit {
  private priceChart: Chart | undefined;
  private costChart: Chart | undefined;
  private usageChart: Chart | undefined;
  comparisonData: number[] = []; // Array to store comparison data

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.createPriceChart(); // Create the hardcoded price chart immediately
    this.fetchDataAndCreateCharts(); // Fetch and create dynamic cost and usage charts
    this.fetchComparisonData(); // Fetch comparison data
  }

  ngAfterViewInit(): void {
    // Ensure the DOM is fully rendered before creating charts
  }

  fetchComparisonData(): void {
    this.apiService.getComparison().subscribe({
      next: (data: number[]) => {
        this.comparisonData = data; // Store the comparison data
      },
      error: (error) => {
        console.error('Error fetching comparison data:', error);
      }
    });
  }

  fetchDataAndCreateCharts(): void {
    // Fetch energy cost data
    this.apiService.getEnergyCost().subscribe({
      next: (energyCostData: number[]) => {
        this.createCostChart(energyCostData);
      },
      error: (error) => {
        console.error('Error fetching energy cost data:', error);
      }
    });

    // Fetch consumption data
    this.apiService.getConsumption().subscribe({
      next: (consumptionData: number[]) => {
        this.createUsageChart(consumptionData);
      },
      error: (error) => {
        console.error('Error fetching consumption data:', error);
      }
    });
  }

  createPriceChart(): void {
    const ctx = document.getElementById('priceChart') as HTMLCanvasElement;
    this.priceChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: [0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
            0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905],
          backgroundColor: '#00A3E0',
          borderRadius: 5
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        responsive: true,
        maintainAspectRatio: false, // Allow custom sizing
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

  createCostChart(data: number[]): void {
    const ctx = document.getElementById('costChart') as HTMLCanvasElement;
    this.costChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: data,
          borderColor: '#fa4616',
          fill: true,
          backgroundColor: 'rgba(250, 71, 22, 0.36)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Allow custom sizing
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

  createUsageChart(data: number[]): void {
    const ctx = document.getElementById('usageChart') as HTMLCanvasElement;
    this.usageChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        datasets: [{
          data: data,
          borderColor: '#005F8C',
          fill: true,
          backgroundColor: 'rgba(0, 96, 140, 0.34)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Allow custom sizing
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

  // Optional: Clean up charts on component destruction to prevent memory leaks
  ngOnDestroy(): void {
    if (this.priceChart) {
      this.priceChart.destroy();
    }
    if (this.costChart) {
      this.costChart.destroy();
    }
    if (this.usageChart) {
      this.usageChart.destroy();
    }
  }
}