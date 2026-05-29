import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { Distributor } from '../../../core/models';

@Component({
  selector: 'app-distributor-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './distributor-detail.html',
})
export class DistributorDetailComponent implements OnInit {
  item: Distributor | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const email = this.route.snapshot.params['id'];
    this.api.getDistributor(email).subscribe(data => (this.item = data));
  }
}
