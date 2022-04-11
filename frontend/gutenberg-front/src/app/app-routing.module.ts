import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BookViewComponent } from './book-view/book-view.component';
import { HomeComponent } from './home/home.component';
import { SearchResultComponent } from './search-result/search-result.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'search',
    component: SearchResultComponent
  },
  {
    path: 'book/:book_id',
    component: BookViewComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
