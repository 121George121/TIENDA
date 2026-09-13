import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { Temporada } from '../../../../models/cu6_gestionar_clasificacion_prendas/clasificacion.model';

export type EntityType = 'categoria' | 'temporada' | 'coleccion';

export interface ClasificacionFormDialogData {
  type: EntityType;
  item?: any;
  isEdit: boolean;
  temporadas?: Temporada[];
}

@Component({
  selector: 'app-clasificacion-form-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule
  ],
  templateUrl: './clasificacion-form-dialog.component.html',
  styleUrls: ['./clasificacion-form-dialog.component.css']
})
export class ClasificacionFormDialogComponent implements OnInit {
  form!: FormGroup;
  type: EntityType;
  isEdit: boolean;
  item?: any;
  temporadas: Temporada[] = [];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<ClasificacionFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ClasificacionFormDialogData
  ) {
    this.type = data.type;
    this.isEdit = data.isEdit;
    this.item = data.item;
    this.temporadas = data.temporadas || [];
  }

  ngOnInit(): void {
    if (this.type === 'categoria') {
      this.form = this.fb.group({
        nombre: [this.item?.nombre || '', [Validators.required, Validators.minLength(3)]],
        descripcion: [this.item?.descripcion || '']
      });
    } else if (this.type === 'temporada') {
      this.form = this.fb.group({
        nombre: [this.item?.nombre || '', [Validators.required, Validators.minLength(3)]],
        descripcion: [this.item?.descripcion || ''],
        fechainicio: [this.item?.fechainicio || ''],
        fechafin: [this.item?.fechafin || '']
      });
    } else if (this.type === 'coleccion') {
      this.form = this.fb.group({
        nombre: [this.item?.nombre || '', [Validators.required, Validators.minLength(3)]],
        descripcion: [this.item?.descripcion || ''],
        imagenurl: [this.item?.imagenurl || ''],
        temporadaid: [this.item?.temporadaid || null]
      });
    }
  }

  get title(): string {
    const action = this.isEdit ? 'Editar' : 'Registrar';
    if (this.type === 'categoria') return `${action} Categoría de Moda`;
    if (this.type === 'temporada') return `${action} Temporada`;
    return `${action} Colección Exclusiva`;
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.dialogRef.close(this.form.value);
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}
