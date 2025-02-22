import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ThemeOption {
  name: string;
  value: string;
  color: string;
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
            <option value="EUR">EUR (€)</option>
            <option value="USD">USD ($)</option>
            <option value="GBP">GBP (£)</option>
          </select>
        </div>
      </div>

      <button class="save-button" (click)="saveSettings()">Save Changes</button>
    </div>
  `,
  styles: [`
    .settings-container {
      background: white;
      border-radius: 16px;
      padding: 30px;
      max-width: 800px;
      margin: 0 auto;
    }

    .settings-section {
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 1px solid #eee;
    }

    .settings-section h3 {
      margin-bottom: 20px;
      color: #333;
    }

    .form-group {
      margin-bottom: 20px;
    }

    .form-group label {
      display: block;
      margin-bottom: 8px;
      color: #666;
    }

    .form-input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 14px;
    }

    .theme-options {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 15px;
    }

    .theme-option {
      padding: 15px;
      border-radius: 8px;
      border: 2px solid transparent;
      cursor: pointer;
      text-align: center;
    }

    .theme-option.active {
      border-color: #4c6fff;
    }

    .theme-color {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      margin: 0 auto 10px;
    }

    .theme-name {
      font-size: 14px;
      color: #666;
    }

    .checkbox-label {
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
    }

    .save-button {
      background: #4c6fff;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
      width: 100%;
    }

    .save-button:hover {
      background: #3b5bff;
    }
  `]
})
export class ProfileComponent {
  themes: ThemeOption[] = [
    { name: 'Blue', value: 'blue', color: '#4c6fff' },
    { name: 'Green', value: 'green', color: '#2ecc71' },
    { name: 'Purple', value: 'purple', color: '#9b59b6' },
    { name: 'Orange', value: 'orange', color: '#e67e22' }
  ];

  profile = {
    name: 'Jenifer Feroz',
    email: 'jenifer@example.com',
    theme: 'blue',
    notifications: {
      email: true,
      push: true
    },
    currency: 'USD',
    costPerKwh: 0.12
  };

  selectTheme(theme: ThemeOption) {
    this.profile.theme = theme.value;
  }

  saveSettings() {
    // Here you would typically save to a backend
    console.log('Saving settings:', this.profile);
    alert('Settings saved successfully!');
  }
}