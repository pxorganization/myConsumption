import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule],
    template: `
        <div class="card">
          <h3>Device Allocation</h3>
          <img src="http://127.0.0.1:8000/image" alt="Device Allocation Chart" class="chart-image" />
        </div>
    `,
    styles: [`
        .chart-image {
            width: 100%;
            display: block;
            margin: 0 auto;
        }
    `]
})
export class ScheduleComponent implements OnInit {
    ngOnInit() {}
}

