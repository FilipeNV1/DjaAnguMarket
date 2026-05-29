import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Warehouse } from '../../../core/models';

@Component({
  selector: 'app-warehouse-detail',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './warehouse-detail.html',
})
export class WarehouseDetailComponent implements OnInit {
  item: Warehouse | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.api.getWarehouse(id).subscribe(data => (this.item = data));
  }
}
