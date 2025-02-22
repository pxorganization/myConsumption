import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="sidebar">
      <div class="logo">myConsumption</div>
      <nav>
        <a routerLink="/consumption" routerLinkActive="active">
          <i class="fas fa-chart-line"></i>
          Consumption
        </a>
        <a routerLink="/scheduling" routerLinkActive="active">
          <i class="fas fa-calendar"></i>
          Scheduling
        </a>

        <div class="nav-item">
          <a routerLink="/devices" routerLinkActive="active">
            <i class="fas fa-plug"></i>
            Devices
          </a>
          <div class="submenu">
            <a routerLink="/devices/add" routerLinkActive="active" class="submenu-item">
              <i class="fas fa-plus"></i>
              Add Device
            </a>
          </div>
        </div>



        <a routerLink="/profile" routerLinkActive="active">
          <i class="fas fa-user"></i>
          Profile
        </a>
      </nav>
    </div>

    <div class="stats-card">
      <div class="stat-box">
        <h3>Total Energy Cost</h3>
        <div class="amount">2,458.32€ </div>
        <div class="change increase">
          <i class="fas fa-arrow-down"></i>
          12.5% from last month
        </div>
      </div>
      
      <div class="stat-box">
        <h3>Total Waiting Time</h3>
        <div class="amount">4.2 hours</div>
        <div class="change increase">
          <i class="fas fa-arrow-down"></i>
          8.3% from last month
        </div>
      </div>
    </div>

    
  `,
  styles: [`
    .sidebar {
      width: 250px;
      background: white;
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 20px;
    }
    

    .logo {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 2rem;
      color: #fa4616;
    }

    nav {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    nav a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px;
      text-decoration: none;
      color: #666;
      border-radius: 8px;
      transition: all 0.3s ease;
    }

    nav a:hover {
      background: #f5f7ff;
      color:rgba(250, 71, 22, 0.77);
    }

    nav a.active {
      background: #fa4616;
      color: white;
      /*#50c5f7#4aba9e*/
    }

    nav i {
      width: 20px;
    }

    .nav-item {
      position: relative;
    }

    .submenu {
      margin-left: 20px;
      margin-top: 5px;
    }

    .submenu-item {
      padding: 8px 12px !important;
      font-size: 0.9em;
    }

    .submenu-item i {
      font-size: 0.9em;
    }
  `]
})
export class SidebarComponent {}