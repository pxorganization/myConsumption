import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule],
    template: `
        <div class="card">
          <h3>Device Allocation</h3>
          <img src="assets/bar_chart.png" alt="Device Allocation Chart" class="chart-image" />
        </div>
    `,
    styles: [`
        .card {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .chart-image {
            width: 100%;
            display: block;
            margin: 0 auto;
        }
    `]
})
export class SchedulingComponent implements OnInit { 
    ngOnInit() {}
}