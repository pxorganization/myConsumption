import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ThemeOption {
  name: string;
  value: string;
  color: string;
  description: string;
  features: string[];
}

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="settings-container">
      <h2>Profile Settings</h2>
      
      <div class="settings-section">
        <h3>Personal Information</h3>
        <div class="form-group">
          <label>Name</label>
          <input type="text" [(ngModel)]="profile.name" class="form-input">
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" [(ngModel)]="profile.email" class="form-input">
        </div>
      </div>

      <div class="settings-section">
        <h3>Plans</h3>
        <div class="theme-options">
          <div *ngFor="let theme of themes" 
               class="theme-option" 
               [class.active]="theme.value === profile.theme"
               [style.background]="theme.color">
            <div class="theme-header">
              <div class="theme-name">{{ theme.name }}</div>
              <div class="theme-description">{{ theme.description }}</div>
            </div>
            <div class="theme-features">
              <div class="feature" *ngFor="let feature of theme.features">
                <i class="fas fa-check-circle"></i>
                {{ feature }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="settings-section">
        <h3>Notifications</h3>
        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" [(ngModel)]="profile.notifications.email">
            Email Notifications
          </label>
        </div>
        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" [(ngModel)]="profile.notifications.push">
            Push Notifications
          </label>
        </div>
      </div>

      <div class="settings-section">
        <h3>Energy Cost Settings</h3>
        <div class="form-group">
          <label>Currency</label>
          <select [(ngModel)]="profile.currency" class="form-input">
            <option value="USD">USD ($)</option>
            <option value="EUR">EUR (€)</option>
            <option value="GBP">GBP (£)</option>
          </select>
        </div>
      </div>

      <button class="save-button" (click)="saveSettings()">Save Changes</button>
    </div>
  `,
  styles: [`
    .theme-options {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }

    .theme-option {
      padding: 25px;
      border-radius: 16px;
      cursor: pointer;
      color: white;
      display: flex;
      flex-direction: column;
      gap: 20px;
      min-height: 400px;
      transition: transform 0.2s;
      position: relative;
      overflow: hidden;
    }

    .theme-option:hover {
      transform: translateY(-5px);
    }

    .theme-option.active::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      border: 5px solid, rgb(0, 0, 0);
      border-radius: 16px;
      pointer-events: none;
    }

    .theme-header {
      text-align: left;
    }

    .theme-name {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 10px;
      color: white;
      font-family: "Poppins", serif;
    }

    .theme-description {
      font-size: 16px;
      opacity: 0.9;
      margin-bottom: 20px;
    }

    .theme-features {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 15px;
    }

    .feature {
      display: flex;
      gap: 10px;
      font-size: 14px;
      text-align: left;
    }

    .feature i {
      color: white;
    }

    .theme-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
      color: white;
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
      font-weight: 500;
      transition: all 0.2s;
    }

    .theme-button:hover {
      background: white;
      color: #333;
    }

    .settings-container {
      max-width: 1200px;
    }

    @media (max-width: 1200px) {
      .theme-options {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    @media (max-width: 768px) {
      .theme-options {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class ProfileComponent {
  themes: ThemeOption[] = [
    { 
      name: 'myHomeEnter',
      value: 'blue',
      color: 'linear-gradient(45deg, #0052D4, #4364F7, #6FB1FC)',
      description: 'Stable pricing for 12 months',
      features: [
        'Fixed rate of 0.145 €/kWh for 12 months',
        'Fixed fee of 5 € per month'
      ]
    },
    { 
      name: 'G1/G1N',
      value: 'green',
      color: 'linear-gradient(45deg, #11998e, #38ef7d)',
      description: 'Monthly price adjustments',
      features: [
        'For homes with dual-zone meters: 0.13089 €',
        'For homes without dual-zone meters:',
        'Fixed fee of 5 € per month',
        'Consumption <= 500 kWh with cost of 0.1548 €',
        'Consumption > 500 kWh with cost of 0.16246 €'
      ]
    },
    { 
      name: 'myHome4All',
      value: 'yellow',
      color: 'linear-gradient(45deg, #FFC312,rgb(247, 240, 31))',
      description: 'Floating pricing per month',
      features: [
        'For homes with dual-zone meters: 0.12882 €',
        'For homes without dual-zone meters:',
        'Fixed fee of 5 € per month',
        'First 500 kWh of the month with cost of 0.14541 €',
        'Rest of kWh of the month with the cost of 0.18114 €'
      ]
    },
    { 
      name: 'Upcoming...',
      value: 'orange',
      color: 'linear-gradient(45deg, #FF8008, #FFC837)',
      description: 'Real-time electricity prices per hour',
      features: [
        'Direct access to wholesale rates',
        'Real-time price monitoring',
        'Smart consumption alerts',
        'Automated usage optimization',
        'Market trend analysis'
      ]
    }
  ];

  profile = {
    name: 'Light Wave',
    email: 'lightwave@example.com',
    theme: 'orange', // Preselected orange plan
    notifications: {
      email: true,
      push: true
    },
    currency: 'EUR'
  };

  saveSettings() {
    console.log('Saving settings:', this.profile);
    alert('Settings saved successfully!');
  }
}