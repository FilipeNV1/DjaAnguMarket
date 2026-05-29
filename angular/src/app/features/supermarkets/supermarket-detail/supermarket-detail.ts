import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { Supermarket } from '../../../core/models';

@Component({
  selector: 'app-supermarket-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './supermarket-detail.html',
})
export class SupermarketDetailComponent implements OnInit {
  item: Supermarket | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.api.getSupermarket(id).subscribe(data => (this.item = data));
  }
}
