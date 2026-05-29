import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { Client } from '../../../core/models';

@Component({
  selector: 'app-client-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './client-detail.html',
})
export class ClientDetailComponent implements OnInit {
  item: Client | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const nif = +this.route.snapshot.params['id'];
    this.api.getClient(nif).subscribe(data => (this.item = data));
  }
}
