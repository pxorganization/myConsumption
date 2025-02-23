import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../services/api.service'; // Import the ApiService from the correct location

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
        <div class="amount">{{ totalEnergyCost | currency:'EUR':'symbol':'1.2-2' }}</div>
      </div>
      
      <div class="stat-box">
  <h3>Total Waiting Time</h3>
  <div class="amount">{{ getFormattedTime(totalWaitingTime) }}</div>
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
      color: rgba(250, 71, 22, 0.77);
    }

    nav a.active {
      background: #fa4616;
      color: white;
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


export class SidebarComponent implements OnInit {
  totalEnergyCost: number = 0;
  totalWaitingTime: number = 0;

  getFormattedTime(minutes: number): string {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    const formattedMinutes = remainingMinutes < 10 ? `0${remainingMinutes}` : remainingMinutes;
    return `${hours}:${formattedMinutes} hours`;
  }

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    // Fetch total energy cost
    this.apiService.getTotalCost().subscribe({
      next: (cost: number) => {
        this.totalEnergyCost = cost;
      },
      error: (error) => {
        console.error('Error fetching total energy cost:', error);
      }
    });

    // Fetch total waiting time
    this.apiService.getTotalWaitingTime().subscribe({
      next: (time: number) => {
        this.totalWaitingTime = time;
      },
      error: (error) => {
        console.error('Error fetching total waiting time:', error);
      }
    });
  }
}