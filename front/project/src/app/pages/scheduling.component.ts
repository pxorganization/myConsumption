import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScheduleComponent } from '../components/schedule.component';

@Component({
  selector: 'app-consumption',
  standalone: true,
  imports: [CommonModule, ScheduleComponent],
  template: `
    <app-dashboard></app-dashboard>
  `
})
export class SchedulingComponent {}