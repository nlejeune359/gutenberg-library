import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { BackendService } from '../services/backend/backend.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  username: string | null = null

  formControl = new FormControl('')

  constructor(private back: BackendService,
    private router: Router) {
    this.username = localStorage.getItem('username')
  }

  ngOnInit(): void {
  }


  newUser() {
    const name = this.formControl.value
    if(name != '') {
      this.back.createUser(name).subscribe(
        user => {
          localStorage.setItem('username', name)
          localStorage.setItem('id', user[name])
          this.username = name
        }
      )
    }
  }

  home() {
    this.router.navigate(['/home'])
  }
}
