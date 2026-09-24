import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatrixBackground } from './matrix-background';

describe('MatrixBackground', () => {
  let component: MatrixBackground;
  let fixture: ComponentFixture<MatrixBackground>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatrixBackground],
    }).compileComponents();

    fixture = TestBed.createComponent(MatrixBackground);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
