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
        <h3>Plans</h3>
        <div class="theme-options">
          <div *ngFor="let theme of themes" 
               class="theme-option" 
               [class.active]="theme.value === profile.theme"
               (click)="selectTheme(theme)">
            <div class="theme-color" [style.background-color]="theme.color"></div>
            <div class="theme-name">{{ theme.name }}</div>
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
  `
})
export class ProfileComponent {
  themes: ThemeOption[] = [
    { name: 'Blue', value: 'blue', color: '#4c6fff' },
    { name: 'Green', value: 'green', color: '#2ecc71' },
    { name: 'Purple', value: 'purple', color: '#9b59b6' }
  ];

  profile = {
    name: 'Jenifer Feroz',
    email: 'jenifer@example.com',
    theme: 'blue',
    notifications: {
      email: true,
      push: true
    },
    currency: 'EUR'
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