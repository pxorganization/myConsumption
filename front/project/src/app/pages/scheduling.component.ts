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
            
            <!-- Πίνακας για τα δεδομένα -->
            <table class="data-table">
                <thead>
                    <tr>
                        <th class="table-header">Device</th>
                        <th class="table-header">Start Time</th>
                        <th class="table-header">End Time</th>
                    </tr>
                </thead>
                <tbody>
                    <tr *ngFor="let device of devices">
                        <td>{{ device.name }}</td>
                        <td>{{ device.startTime }}</td>
                        <td>{{ device.endTime }}</td>
                    </tr>
                </tbody>
            </table>
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

        .data-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }

        .data-table th, .data-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        .table-header {
            background-color: #fa4616; /* Πορτοκαλί χρώμα για την κεφαλίδα */
            color: white; /* Λευκό χρώμα γραμματοσειράς για καλύτερη ανάγνωση */
            font-weight: bold; /* Έντονη γραμματοσειρά */
        }
    `]
})
export class SchedulingComponent implements OnInit {
    
    solution = {
        "Dish Washer": [857, 977],
        "Washing Machine": [611, 701],
        "Cloth Dryer": [1084, 1174],
        "Oven 1": [1114, 1204],
        "Oven 2": [722, 812],
        "Cook Top": [1140, 1170],
        "Microwave": [516, 528],
        "Electric Vehicle": [1390, 190], // 1390 + 240 = 1630 and to start from 0 i do 1630 - 1440 = 190
        "Laptop": [1028, 1148],
        "Vacuum Cleaner": [641, 701],
        "Air Condition 1": [480, 570],
        "Air Condition 2": [1156, 1246],
        "Water Heater": [1023, 1143],
        "Refrigerator": [0, 1440],
        "Lighting 1": [420, 600],
        "Lighting 2": [1080, 60]
    };

    
    devices: { name: string, startTime: string, endTime: string }[] = [];

    ngOnInit() {
        this.devices = this.transformSolution(this.solution);
    }

    
    convertMinutesToTime(minutes: number): string {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
    }

    transformSolution(solution: { [key: string]: number[] }): { name: string, startTime: string, endTime: string }[] {
        const devices = [];
        for (const [name, times] of Object.entries(solution)) {
            devices.push({
                name: name,
                startTime: this.convertMinutesToTime(times[0]),
                endTime: this.convertMinutesToTime(times[1])
            });
        }
        return devices;
    }
}