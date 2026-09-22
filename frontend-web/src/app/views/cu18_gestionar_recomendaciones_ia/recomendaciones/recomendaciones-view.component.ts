import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { RecomendacionController } from '../../../controllers/cu18_gestionar_recomendaciones_ia/recomendacion.controller';

@Component({
  selector: 'app-recomendaciones-view',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatChipsModule,
    MatDividerModule
  ],
  templateUrl: './recomendaciones-view.component.html',
  styleUrls: ['./recomendaciones-view.component.css']
})
export class RecomendacionesViewComponent implements OnInit {
  constructor(public controller: RecomendacionController) {}

  ngOnInit(): void {
    this.controller.cargarTendencias();
    this.controller.generarRecomendacionOutfit();
  }
}
