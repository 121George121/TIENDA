import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent as LegacyDashboardComponent } from '../../dashboard/dashboard.component';

@Component({
  selector: 'app-cu27-dashboard-ejecutivo',
  standalone: true,
  imports: [CommonModule, LegacyDashboardComponent],
  template: `<app-dashboard></app-dashboard>`
})
export class DashboardEjecutivoComponent {}
