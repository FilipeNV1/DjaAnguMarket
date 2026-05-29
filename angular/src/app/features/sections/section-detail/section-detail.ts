import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/services/api.service';
import { Section } from '../../../core/models';

@Component({
  selector: 'app-section-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './section-detail.html',
})
export class SectionDetailComponent implements OnInit {
  item: Section | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const sname = this.route.snapshot.params['id'];
    this.api.getSection(sname).subscribe(data => (this.item = data));
  }
}
