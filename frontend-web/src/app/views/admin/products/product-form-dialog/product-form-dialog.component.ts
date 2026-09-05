import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { Producto } from '../../../../models/product.model';
import { Categoria } from '../../../../models/clasificacion.model';

export interface ProductFormDialogData {
  producto?: Producto;
  isEdit: boolean;
  categorias: Categoria[];
}

@Component({
  selector: 'app-product-form-dialog',
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
  templateUrl: './product-form-dialog.component.html',
  styleUrls: ['./product-form-dialog.component.css']
})
export class ProductFormDialogComponent implements OnInit {
  form!: FormGroup;
  isEdit: boolean;
  producto?: Producto;
  categorias: Categoria[] = [];

  generosList: string[] = ['Damas', 'Caballeros', 'Unisex', 'Niños'];
  gruposEdadList: string[] = ['Adultos', 'Juvenil', 'Infantil'];

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<ProductFormDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: ProductFormDialogData
  ) {
    this.isEdit = data.isEdit;
    this.producto = data.producto;
    this.categorias = data.categorias || [];
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      nombre: [this.producto?.nombre || '', [Validators.required, Validators.minLength(3)]],
      descripcion: [this.producto?.descripcion || ''],
      marca: [this.producto?.marca || 'Boutique Collection', [Validators.required]],
      genero: [this.producto?.genero || 'Damas', [Validators.required]],
      grupoedad: [this.producto?.grupoedad || 'Adultos'],
      preciobase: [this.producto?.preciobase || 0, [Validators.required, Validators.min(0)]],
      imagenprincipal: [this.producto?.imagenprincipal || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600'],
      categoriaid: [this.producto?.categoriaid || null]
    });
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
