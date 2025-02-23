import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators'; 

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8001'; 

  constructor(private http: HttpClient) {}

  getTotalCost(): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/getTotalCost`);
  }

  getTotalWaitingTime(): Observable<number> {
    return this.http.get<number>(`${this.apiUrl}/getTotalWaitingTime`);
  }
  
  getEnergyCost(): Observable<number[]> {
    return this.http.get<number[]>(`${this.apiUrl}/getEnergyCost`);
  }

  getConsumption(): Observable<number[]> {
    return this.http.get<number[]>(`${this.apiUrl}/getConsumption`);
  }


}