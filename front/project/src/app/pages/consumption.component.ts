import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from '../components/dashboard.component';

@Component({
  selector: 'app-consumption',
  standalone: true,
  imports: [CommonModule, DashboardComponent],
  template: `
    <app-dashboard></app-dashboard>
  `
})
export class ConsumptionComponent {}