import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';
import { Employee } from '../../../core/models';

@Component({
  selector: 'app-employee-detail',
  standalone: true,
  imports: [RouterLink, DecimalPipe],
  templateUrl: './employee-detail.html',
})
export class EmployeeDetailComponent implements OnInit {
  item: Employee | null = null;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.params['id'];
    this.api.getEmployee(id).subscribe(data => (this.item = data));
  }
}
