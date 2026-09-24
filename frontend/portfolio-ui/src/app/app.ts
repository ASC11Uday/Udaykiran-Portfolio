import { Component } from '@angular/core';
import { Navbar } from './components/navbar/navbar';
import { Hero } from './components/hero/hero';
import { About } from './components/about/about';
import { Experience } from './components/experience/experience';
import { Projects } from './components/projects/projects';
import { Skills } from './components/skills/skills';
import { Contact } from './components/contact/contact';
import { LoadingScreen } from './components/loading-screen/loading-screen';
import { CustomCursor } from './components/custom-cursor/custom-cursor';
import { Footer } from './components/footer/footer';

@Component({
  selector: 'app-root',
  imports: [Navbar, Hero, About, Experience, Projects, Skills, Contact, LoadingScreen, CustomCursor,Footer],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  isLoading = true;

onLoadingComplete(): void {
  this.isLoading = false;
}

}