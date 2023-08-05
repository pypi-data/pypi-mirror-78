// Copyright 2008-2016 Conrad Sanderson (http://conradsanderson.id.au)
// Copyright 2008-2016 National ICT Australia (NICTA)
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ------------------------------------------------------------------------


//! \addtogroup arma_rel_comparators
//! @{



template<typename eT>
struct arma_lt_comparator
  {
  arma_inline bool operator() (const eT a, const eT b) const { return (a < b); }
  };



template<typename eT>
struct arma_gt_comparator
  {
  arma_inline bool operator() (const eT a, const eT b) const { return (a > b); }
  };



template<typename eT>
struct arma_leq_comparator
  {
  arma_inline bool operator() (const eT a, const eT b) const { return (a <= b); }
  };
  


template<typename eT>
struct arma_geq_comparator
  {
  arma_inline bool operator() (const eT a, const eT b) const { return (a >= b); }
  };



template<typename T>
struct arma_lt_comparator< std::complex<T> >
  {
  typedef typename std::complex<T> eT;
  
  inline bool operator() (const eT& a, const eT& b) const { return (std::abs(a) < std::abs(b)); }
  
  // inline
  // bool
  // operator() (const eT& a, const eT& b) const
  //   {
  //   const T abs_a = std::abs(a);
  //   const T abs_b = std::abs(b);
  //   
  //   return ( (abs_a != abs_b) ? (abs_a < abs_b) : (std::arg(a) < std::arg(b)) );
  //   }
  };



template<typename T>
struct arma_gt_comparator< std::complex<T> >
  {
  typedef typename std::complex<T> eT;
  
  inline bool operator() (const eT& a, const eT& b) const { return (std::abs(a) > std::abs(b)); }
  
  // inline
  // bool
  // operator() (const eT& a, const eT& b) const
  //   {
  //   const T abs_a = std::abs(a);
  //   const T abs_b = std::abs(b);
  //   
  //   return ( (abs_a != abs_b) ? (abs_a > abs_b) : (std::arg(a) > std::arg(b)) );
  //   }
  };



template<typename T>
struct arma_leq_comparator< std::complex<T> >
  {
  typedef typename std::complex<T> eT;
  
  inline bool operator() (const eT& a, const eT& b) const { return (std::abs(a) <= std::abs(b)); }
  };



template<typename T>
struct arma_geq_comparator< std::complex<T> >
  {
  typedef typename std::complex<T> eT;
  
  inline bool operator() (const eT& a, const eT& b) const { return (std::abs(a) >= std::abs(b)); }
  };



//! @}
