#include "petscsys.h"
#include "petscfix.h"
#include "petsc/private/fortranimpl.h"
/* hpddm.cxx */
/* Fortran interface file */

/*
* This file was generated automatically by bfort from the C source
* file.  
 */

#ifdef PETSC_USE_POINTER_CONVERSION
#if defined(__cplusplus)
extern "C" { 
#endif 
extern void *PetscToPointer(void*);
extern int PetscFromPointer(void *);
extern void PetscRmPointer(void*);
#if defined(__cplusplus)
} 
#endif 

#else

#define PetscToPointer(a) (*(PetscFortranAddr *)(a))
#define PetscFromPointer(a) (PetscFortranAddr)(a)
#define PetscRmPointer(a)
#endif

#include "petscksp.h"
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define ksphpddmsetdeflationspace_ KSPHPDDMSETDEFLATIONSPACE
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define ksphpddmsetdeflationspace_ ksphpddmsetdeflationspace
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define ksphpddmgetdeflationspace_ KSPHPDDMGETDEFLATIONSPACE
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define ksphpddmgetdeflationspace_ ksphpddmgetdeflationspace
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define ksphpddmmatsolve_ KSPHPDDMMATSOLVE
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define ksphpddmmatsolve_ ksphpddmmatsolve
#endif


/* Definitions of Fortran Wrapper routines */
#if defined(__cplusplus)
extern "C" {
#endif
PETSC_EXTERN void  ksphpddmsetdeflationspace_(KSP ksp,Mat U, int *__ierr){
*__ierr = KSPHPDDMSetDeflationSpace(
	(KSP)PetscToPointer((ksp) ),
	(Mat)PetscToPointer((U) ));
}
PETSC_EXTERN void  ksphpddmgetdeflationspace_(KSP ksp,Mat *U, int *__ierr){
*__ierr = KSPHPDDMGetDeflationSpace(
	(KSP)PetscToPointer((ksp) ),U);
}
PETSC_EXTERN void  ksphpddmmatsolve_(KSP ksp,Mat B,Mat X, int *__ierr){
*__ierr = KSPHPDDMMatSolve(
	(KSP)PetscToPointer((ksp) ),
	(Mat)PetscToPointer((B) ),
	(Mat)PetscToPointer((X) ));
}
#if defined(__cplusplus)
}
#endif
