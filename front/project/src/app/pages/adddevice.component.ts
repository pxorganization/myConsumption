import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// interface ThemeOption {
//   name: string;
//   value: string;
//   color: string;
// }

@Component({
  selector: 'app-device',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="settings-container">
      <h2>Add a Device</h2>
      
      <div class="settings-section">
        <h3>Device Information</h3>
        <div class="form-group">
          <label>Name</label>
          <input type="text" [(ngModel)]="profile.name" class="form-input">
        </div>

        <div class="form-group">
          <label>Type</label>
          <select [(ngModel)]="profile.type" class="form-input">
            <option value="Kitchen">Kitchen</option>
            <option value="Living Room">Living Room</option>
            <option value="Bedroom">Bedroom</option>
          </select>
        </div>
      </div>

      <div class="settings-section">
        <h3>Time Details</h3>
        <div class="form-group">
          <label>Estimated Duration in hours</label>
          <input type="text" [(ngModel)]="profile.duration" class="form-input">
        </div>

        <label>Estimated Start Time based on your usage during a day</label>
          <select [(ngModel)]="profile.start" class="form-input">
            <option value="Kitchen">Kitchen</option>
            <option value="Living Room">Living Room</option>
            <option value="Bedroom">Bedroom</option>
          </select>
        </div>

        <label>Estimated End Time on your usage during a day</label>
          <select [(ngModel)]="profile.start" class="form-input">
            <option value="Kitchen">Kitchen</option>
            <option value="Living Room">Living Room</option>
            <option value="Bedroom">Bedroom</option>
          </select>
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
        <div class="form-group">
          <label>Cost per kWh</label>
          <input type="number" [(ngModel)]="profile.costPerKwh" class="form-input">
        </div>
      </div>

      <button class="save-button" (click)="saveSettings()">Save Changes</button>
    </div>
  `
})
export class ProfileComponent {
//   themes: ThemeOption[] = [
//     { name: 'Blue', value: 'blue', color: '#4c6fff' },
//     { name: 'Green', value: 'green', color: '#2ecc71' },
//     { name: 'Purple', value: 'purple', color: '#9b59b6' },
//     { name: 'Orange', value: 'orange', color: '#e67e22' }
//   ];

  profile = {
    name: 'Jenifer Feroz',
    type: 'Living Room',
    plan: 'blue',
    duration: '2',
    start: "14:00",
    end: ""
  };

//   selectTheme(theme: ThemeOption) {
//     this.profile.theme = theme.value;
//   }

  saveSettings() {
    // Here you would typically save to a backend
    console.log('Saving settings:', this.profile);
    alert('Settings saved successfully!');
  }
}