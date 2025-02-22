import { Routes } from '@angular/router';
import { ConsumptionComponent } from './pages/consumption.component';
import { DevicesPageComponent } from './pages/devices-page.component';
import { ProfileComponent } from './pages/profile.component';
import { SchedulingComponent } from './pages/scheduling.component';
import { AddComponent } from './pages/adddevice.component';

export const routes: Routes = [
  { path: '', redirectTo: 'consumption', pathMatch: 'full' },
  { path: 'consumption', component: ConsumptionComponent },
  { path: 'devices', component: DevicesPageComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'scheduling', component: SchedulingComponent },
  { path: 'devices/add', component: AddComponent }
  
];