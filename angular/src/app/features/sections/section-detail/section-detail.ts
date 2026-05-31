import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Section, Product } from '../../../core/models';

@Component({
  selector: 'app-section-detail',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './section-detail.html',
})
export class SectionDetailComponent implements OnInit {

  item: Section | null = null;
  products: Product[] = [];

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const sname = decodeURIComponent(this.route.snapshot.params['id']);
    this.api.getSection(sname).subscribe(data => (this.item = data));
    this.api.getProducts().subscribe(all => {
      this.products = all.filter(p => (p.section ?? p.section_name) === sname);
    });
  }
}