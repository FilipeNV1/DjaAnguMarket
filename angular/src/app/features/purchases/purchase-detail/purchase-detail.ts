import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Purchase } from '../../../core/models';

@Component({
  selector: 'app-purchase-detail',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './purchase-detail.html',
})
export class PurchaseDetailComponent implements OnInit {
  item: Purchase | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.api.getPurchase(id).subscribe(data => (this.item = data));
  }
}
