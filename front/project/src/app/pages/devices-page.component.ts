import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Device {
  id: number;
  name: string;
  icon: string;
  status: boolean;
}

interface HistoryItem {
  device: string;
  time: string;
  action: string;
}

@Component({
  selector: 'app-devices-page',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="display: flex; gap: 20px;">
      <div style="flex: 2;">
        <h2>Devices Right Now</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 35px;">
          <div *ngFor="let device of devices" class="device-card-large">
            <div class="device-status" [class.active]="device.status">
              {{ device.status ? 'On' : 'Off' }}
            </div>
            <div class="device-icon-large">
              <i [class]="device.icon"></i>
            </div>
            <div class="device-name">{{ device.name }}</div>
            <label class="toggle-switch">
              <input type="checkbox" 
                     [checked]="device.status" 
                     (change)="toggleDevice(device)"
                     [id]="'device-' + device.id">
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>
      
      <div style="flex: 1;">
        <h2>History</h2>
        <div class="history-list">
          <div *ngFor="let item of history" class="history-item">
            <div class="history-icon" [ngClass]="getHistoryIconClass(item)">
              <i [class]="getHistoryIcon(item)"></i>
            </div>
            <div class="history-content">
              <div class="history-device">{{ item.device }}</div>
              <div class="history-action">{{ item.action }}</div>
              <div class="history-time">{{ item.time }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .device-card-large {
      background: rgba(255, 255, 255, 0.27);
      border-radius: 16px;
      padding: 15px;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      min-height: 100px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)
    }
    
    .device-status {
      position: absolute;
      top: 15px;
      left: 15px;
      padding: 5px 10px;
      border-radius: 12px;
      background: #f0f0f0;
      font-size: 12px;
    }
    
    .device-status.active {
      background: #e8f5e9;
      color: #2ecc71;
    }
    
    .device-icon-large {
      width: 60px;
      height: 60px;
      background: #e8eeff;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }
    
    .device-name {
      font-weight: 500;
      font-size: 16px;
    }
    
    .history-list {
      background: white;
      border-radius: 16px;
      padding: 20px;
      max-height: 400px;
      overflow-y: auto;
    }
    
    .history-item {
      display: flex;
      gap: 15px;
      padding: 15px 0;
      border-bottom: 1px solid #f0f0f0;
    }
    
    .history-icon {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .history-icon.on {
      background: #e8f5e9;
      color: #2ecc71;
    }
    
    .history-icon.off {
      background: #ffebee;
      color: #e74c3c;
    }
    
    .history-content {
      flex: 1;
    }
    
    .history-device {
      font-weight: 500;
    }
    
    .history-action {
      color: #666;
      font-size: 14px;
    }
    
    .history-time {
      color: #999;
      font-size: 12px;
    }
  `]
})
export class DevicesPageComponent implements OnInit {
  devices: Device[] = [
    { id: 1, name: 'Dish washer', icon: 'fas fa-sink', status: false },
    { id: 2, name: 'Washine machine', icon: 'fas fa-soap', status: false },
    { id: 3, name: 'Cloth Dryer', icon: 'fas fa-tshirt', status: false },
    { id: 4, name: 'Oven 1', icon: 'fas fa-utensils', status: false },
    { id: 5, name: 'Air Conditioner 1', icon: 'fas fa-snowflake', status: false },
    { id: 6, name: 'Cook Top', icon: 'fas fa-utensils', status: false },
    { id: 7, name: 'Microwave', icon: 'fas fa-utensils', status: false },
    { id: 8, name: 'Electric Vehicle', icon: 'fas fa-car', status: true },
    { id: 9, name: 'Laptop', icon: 'fas fa-laptop', status: false },
    { id: 10, name: 'Vacuum cleaner', icon: 'fas fa-broom', status: false },
    { id: 11, name: 'Oven 2', icon: 'fas fa-utensils', status: false },
    { id: 12, name: 'Air Conditioner 2', icon: 'fas fa-snowflake', status: false },
    { id: 13, name: 'Water Heater', icon: 'fas fa-blender', status: false },
    { id: 14, name: 'Refrigerator', icon: 'fas fa-box', status: true },
    { id: 15, name: 'Lighting 1', icon: 'fas fa-lightbulb', status: false },
    { id: 16, name: 'Lighting 2', icon: 'fas fa-lightbulb', status: false },
    
  ];

  history: HistoryItem[] = [
    { device: 'Air Conditioner', time: '03:20', action: 'Turned on' },
    { device: 'Refrigerator', time: '01:45', action: 'Turned on' },
    { device: 'Air Conditioner', time: '11:36', action: 'Turned off' },
    { device: 'Coffee Machine', time: '09:15', action: 'Turned off' }
  ];

  ngOnInit() {
    localStorage.removeItem('devices');

    // Load saved device states from localStorage
    const savedDevices = localStorage.getItem('devices');
    if (savedDevices) {
      this.devices = JSON.parse(savedDevices);
    } else {
      this.saveDeviceStates();
    }

    // Load saved history from localStorage
    const savedHistory = localStorage.getItem('deviceHistory');
    if (savedHistory) {
      this.history = JSON.parse(savedHistory);
    }
  }

  toggleDevice(device: Device) {
    device.status = !device.status;
    this.addToHistory(device);
    this.saveDeviceStates();
  }

  addToHistory(device: Device) {
    const now = new Date();
    const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    const newHistoryItem = {
      device: device.name,
      time: time,
      action: device.status ? 'Turned on' : 'Turned off'
    };

    this.history.unshift(newHistoryItem);
    
    // Keep only the last 50 history items
    if (this.history.length > 50) {
      this.history = this.history.slice(0, 50);
    }

    // Save history to localStorage
    localStorage.setItem('deviceHistory', JSON.stringify(this.history));
  }

  saveDeviceStates() {
    localStorage.setItem('devices', JSON.stringify(this.devices));
  }

  getHistoryIconClass(item: HistoryItem): string {
    return item.action.includes('on') ? 'on' : 'off';
  }

  getHistoryIcon(item: HistoryItem): string {
    return item.action.includes('on') ? 'fas fa-power-off' : 'fas fa-power-off';
  }
}