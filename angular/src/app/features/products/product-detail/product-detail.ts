import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Product } from '../../../core/models';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './product-detail.html',
})
export class ProductDetailComponent implements OnInit {
  item: Product | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.api.getProduct(id).subscribe(data => (this.item = data));
  }

  get sectionName(): string {
    return this.item?.section ?? this.item?.section_name ?? '';
  }
}
