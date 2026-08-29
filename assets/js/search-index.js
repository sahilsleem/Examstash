/**
 * ExamStash Search Index
 * Fast in-memory index of boards, universities, entrance exams, subjects, and papers
 */

window.EXAMSTASH_SEARCH_INDEX = [
  // School Boards
  { title: "JKBOSE Class 10 Question Papers & Syllabus", category: "School Board", icon: "🏫", url: "/jkbose/class-10/", tags: ["jkbose", "class 10", "10th", "matric", "kashmir", "jammu", "board"] },
  { title: "JKBOSE Class 12 Question Papers (All Streams)", category: "School Board", icon: "🏫", url: "/jkbose/class-12/", tags: ["jkbose", "class 12", "12th", "science", "arts", "commerce", "board"] },
  { title: "JKBOSE Main Portal — All Classes", category: "School Board", icon: "🏫", url: "/jkbose/", tags: ["jkbose", "jammu kashmir board", "school"] },
  
  { title: "CBSE Class 10 Previous Year Papers", category: "School Board", icon: "📚", url: "/cbse/class-10/", tags: ["cbse", "class 10", "10th", "ncert", "central board"] },
  { title: "CBSE Class 12 Previous Year Papers", category: "School Board", icon: "📚", url: "/cbse/class-12/", tags: ["cbse", "class 12", "12th", "pcm", "pcb", "commerce"] },
  { title: "CBSE Main Portal — Classes 10 & 12", category: "School Board", icon: "📚", url: "/cbse/", tags: ["cbse", "central board"] },

  { title: "ICSE Class 10 Papers & Syllabus", category: "School Board", icon: "📖", url: "/icse/class-10/", tags: ["icse", "class 10", "10th", "cisce"] },
  { title: "ISC Class 12 Papers & Syllabus", category: "School Board", icon: "📖", url: "/icse/class-12/", tags: ["isc", "class 12", "12th", "cisce"] },
  { title: "ICSE / ISC Main Portal", category: "School Board", icon: "📖", url: "/icse/", tags: ["icse", "isc", "cisce"] },

  // Universities & Colleges
  { title: "Islamia College Srinagar (ICSC) Papers & Syllabi", category: "University", icon: "🏛️", url: "/islamia-college/", tags: ["islamia college", "icsc", "srinagar", "autonomous", "hawal"] },
  { title: "Islamia College — BCA (Bachelor of Computer Applications)", category: "University Course", icon: "💻", url: "/islamia-college/bca/", tags: ["bca", "islamia", "computer", "programming"] },
  { title: "Islamia College — BBA (Bachelor of Business Administration)", category: "University Course", icon: "📊", url: "/islamia-college/bba/", tags: ["bba", "islamia", "management", "business"] },
  { title: "Islamia College — B.Sc (Medical & Non-Medical)", category: "University Course", icon: "🔬", url: "/islamia-college/bsc/", tags: ["bsc", "islamia", "science", "physics", "chemistry", "botany", "zoology"] },
  { title: "Islamia College — B.Com (Bachelor of Commerce)", category: "University Course", icon: "📑", url: "/islamia-college/bcom/", tags: ["bcom", "islamia", "commerce", "accounting"] },
  { title: "Islamia College — B.A (Bachelor of Arts)", category: "University Course", icon: "📚", url: "/islamia-college/ba/", tags: ["ba", "islamia", "arts", "humanities", "political science", "history"] },
  { title: "Islamia College — MBA / MCA / M.Sc / M.Com (PG Courses)", category: "University Course", icon: "🎓", url: "/islamia-college/", tags: ["pg", "postgraduate", "mba", "mca", "mcom", "msc", "islamia"] },

  { title: "Kashmir University (KU) Papers & Notes", category: "University", icon: "🏛️", url: "/kashmir-university/", tags: ["kashmir university", "ku", "hazratbal", "ug", "pg"] },
  { title: "Cluster University Srinagar (CUS)", category: "University", icon: "🏛️", url: "/cluster-university/", tags: ["cluster university", "cus", "srinagar", "integrated"] },
  { title: "BGSBU Rajouri — Question Papers", category: "University", icon: "🏛️", url: "/bgsbu/", tags: ["bgsbu", "baba ghulam shah badshah", "rajouri", "engineering", "diploma"] },

  // Competitive & Entrance Exams
  { title: "NEET UG Past Year Papers & Solution Keys", category: "Competitive Exam", icon: "🩺", url: "/neet/", tags: ["neet", "ug", "medical", "mbbs", "bds", "nta", "biology", "physics", "chemistry"] },
  { title: "JEE Main & Advanced Question Papers", category: "Competitive Exam", icon: "⚡", url: "/jee/", tags: ["jee", "main", "advanced", "iit", "nit", "engineering", "nta", "maths"] },
  { title: "CUET (Common University Entrance Test)", category: "Competitive Exam", icon: "🎯", url: "/cuet/", tags: ["cuet", "ug", "pg", "nta", "central universities"] },
  { title: "JKPSC — KAS / CCE, Assistant Professor, Lecturer", category: "Competitive Exam", icon: "⚖️", url: "/jkpsc/", tags: ["jkpsc", "kas", "cce", "civil services", "assistant professor", "kashmir"] },
  { title: "Competitive & Entrance Exams Portal", category: "Competitive Exam", icon: "🏆", url: "/competitive/", tags: ["competitive", "entrance", "exams", "all"] },

  // Specific Real Question Papers
  { title: "JKBOSE Class 10 Mathematics Question Paper 2026 (Series A)", category: "Question Paper", icon: "📐", url: "/jkbose/class-10/maths/2026/series-a/", tags: ["jkbose", "class 10", "maths", "mathematics", "2026", "series a", "annual"] },
  { title: "JKBOSE Class 10 Mathematics Question Paper 2026 (Series B)", category: "Question Paper", icon: "📐", url: "/jkbose/class-10/maths/2026/series-b/", tags: ["jkbose", "class 10", "maths", "mathematics", "2026", "series b", "annual"] },
  { title: "JKBOSE Class 10 Mathematics Question Paper 2026 (Series C)", category: "Question Paper", icon: "📐", url: "/jkbose/class-10/maths/2026/series-c/", tags: ["jkbose", "class 10", "maths", "mathematics", "2026", "series c", "annual"] },
  { title: "JKBOSE Class 10 Mathematics Question Paper 2023", category: "Question Paper", icon: "📐", url: "/jkbose/class-10/maths/2023/", tags: ["jkbose", "class 10", "maths", "mathematics", "2023", "annual"] },
  { title: "JKBOSE Class 10 Science Question Paper 2026 (Series A)", category: "Question Paper", icon: "🔬", url: "/jkbose/class-10/science/2026/series-a/", tags: ["jkbose", "class 10", "science", "2026", "series a", "physics", "chemistry", "biology"] },
  { title: "JKBOSE Class 10 Science Question Paper 2026 (Series B)", category: "Question Paper", icon: "🔬", url: "/jkbose/class-10/science/2026/series-b/", tags: ["jkbose", "class 10", "science", "2026", "series b"] },
  { title: "JKBOSE Class 10 English Question Paper 2026 (Series C)", category: "Question Paper", icon: "📝", url: "/jkbose/class-10/english/2026/series-c/", tags: ["jkbose", "class 10", "english", "2026", "series c"] },
  { title: "JKBOSE Class 10 Social Science Question Paper 2026 (Series A)", category: "Question Paper", icon: "🌍", url: "/jkbose/class-10/social-science/2026/series-a/", tags: ["jkbose", "class 10", "social science", "sst", "2026", "series a"] }
];
