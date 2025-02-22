import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

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
          <input type="text" [(ngModel)]="profile.name" class="form-input" placeholder="Enter device name">
        </div>

        <div class="form-group">
          <label>Type</label>
          <select [(ngModel)]="profile.type" class="form-input">
            <option value="" disabled selected>Select a room type</option>
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
          <input type="text" [(ngModel)]="profile.duration" class="form-input" placeholder="e.g., 2">
        </div>

        <div class="form-group">
          <label>Estimated Start Time based on your usage during a day</label>
          <input type="text" [(ngModel)]="profile.start" class="form-input" placeholder="HH:MM (24hr format)">
        </div>

        <div class="form-group">
          <label>Estimated End Time based on your usage during a day</label>
          <input type="text" [(ngModel)]="profile.end" class="form-input" placeholder="HH:MM (24hr format)">
        </div>

      </div>

      <button class="save-button" (click)="saveSettings()">Add Device</button>
    </div>
  `
})
export class AddComponent {
  profile = {
    name: '',
    type: '',
    duration: '',
    start: '',
    end: ''
  };

  saveSettings() {
    // Here you would typically save to a backend
    console.log('Saving settings:', this.profile);
    alert('Settings saved successfully!');
  }
}