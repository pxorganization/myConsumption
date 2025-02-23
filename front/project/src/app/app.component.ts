import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from './components/sidebar.component';
import { HttpClientModule } from '@angular/common/http'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent, HttpClientModule], 
  template: `
    <div style="display: flex; padding: 20px; gap: 40px;">
      <app-sidebar></app-sidebar>
      <div style="flex: 1;">
        <router-outlet></router-outlet>
      </div>
    </div>
  `
})
export class App {
  title = 'Energy Monitoring';
}