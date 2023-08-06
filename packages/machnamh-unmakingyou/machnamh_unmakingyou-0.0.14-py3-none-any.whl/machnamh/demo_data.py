class demo_data():

	def __init__(self):
		self.html = """

		<br><font size="6"> <span style="color:green">About the Law School Admission data:</span><br>
		<font size="2">

		The Law School Admission Council surveyed 163 law schools in the United States.
		The dataset contains information on 21,790 law students over five years starting from 
		1991. For three years the study tracked those students who entered law school in 
		Autumn 1991 in addition to tracking up to 5 rounds of the students' BAR examinations.
		Note that the original purpose of gathering this data was not to create a machine 
		learning model, however, the data does serve as a good example of how existing data
		might be used for such a purpose and of the necessity to reflect upon the use of such 
		data for the creation of decision-making models which have real-world consequences on 
		humans. <br><br>

		The data includes:

		<ul>
		<li><b>UGPA (Undergraduate grade point average):</b> The undergraduate grade-point 
		average collected before law school. GPA is a standard way of measuring academic
		achievement in the U.S. Each course is given a certain number of "credits". 
		In secondary school it is usual for all courses/subjects to have the same 
		number of credits, college or university courses however can have between 1 and 5 
		credits per course, the average is 3 which corresponds to 3 hours of lectures and 
		approx 6 hours of homework per week. GPA assumes a grading scale of A, B, C, D, F, each of which is assigned a number of grade points.
		A=4, B=3, C=2, D=1, F=0. The GPA is the (sum of the credits x grade)/sum of the credits. 
		e.g a 3 credit class with A grade and a 4 credit class with a C grade would result in (3*4+4*2)/(3+4)
		</li>

		<li><b>LSAT (Law school admissions test):</b> The Law School Admission Test is an
		integral part of law school admission in the United States, Canada and several
		other countries, according to the admissions council the test is designed to 
		assess critical reading, analytical reasoning, logical reasoning, and persuasive
		writing skills which are the skills deemed necessary to succeed in law school.
		Some Law schools do accept other tests, however, as of 2020, the LSAT remains
		the dominant test for law school admission. The sponsors of the LSAT (The Law School
		admissions council) suggest that it is a useful measure for predicting first-year 
		average grades or the likelihood of passing the BAR exam. </li>

		<li><b>sander_index:</b> Sander proposes combining the LSAT and GPA scores into a 
		single weighted average, using weights that correspond roughly to those used 
		in many law schools. This average is referred to as the “Sander Index.” Because
		the units of this index are difficult to interpret it has been converted into a 
		percentile score. This score ranges from 0 to 100 and represents the percentage 
		of law school matriculants with lower index scores. That is, a student with a 
		percentile score of 75 has better academic credentials than three-quarters of
		law school matriculants, but worse credentials than the remaining quarter. 
		</li>
		   
		<li><b>ZFYA (Z-score of First-year average grade): </b> This is a measure of first-year
		academic achievement in law school, presented as a z-score. 
		Z-Scores are raw scores expressed in standard deviation units, relative to the mean score. 
		<ul>
		<li>Positive Z‐scores indicate a raw score that is above the mean.</li>
		<li>Negative Z‐scores indicate a raw score that is below the mean.</li>
		<li>Zero Z‐score indicates a raw score that is equal to the mean.</li>
		</ul>

		In a normally‐distributed set of data, the general rule states that 68% of all scores will fall 
		within ±1 SD of the mean; 95% of all scores will fall within ±2 SD, and 99.7% of all scores within ±3 
		SD. Z‐scores between ‐2.00 and +2.00 are therefore considered relatively ordinary, while
		values greater than ‐2.00 and +2.00 are considered unusual.</li>
		 
		<li><b>first_pf:</b> Whether or not the BAR exam was passed or failed on the first attempt, the BAR exam 
		is facilitated by the American Bar Association and apparently designed to test knowledge and skills 
		that every lawyer should have before becoming licensed to practice law. It is worth noting that in most states, 
		a law school graduate cannot take the bar exam without having attended a law school accredited by
		the American Bar Association(ABA).
		</li>

		<li><b>Region_first:</b> The geographic region in which the first BAR exam was taken. The jurisdictions 
		used in this study match those used by the Law School Admission Council(LSAC) in Regional Statistical Reports. 
		Definitions of regional groups are: 
		<ul><li> New England[NG] and Northeast[NE].</li>
		<li>Midsouth[MS], Southeast[SE], and South Central[SC] (South)</li>
		<li> Northwest[NW], Far West[FW], and Mountain West[Mt](West)</li>
		<li> Great Lakes[GL] and Midwest[MW].</li>
		</ul>
		A feature such as this might be used as an intentional proxy for the geographical 
		location of the student, or an unintentional proxy for the race of a student.
		</li>
		<li><b>Race</b> The race of the students has been categorised as 'White', 'Hispanic', 'Asian', 'Black', 
		'Other', 'Mexican', 'Puertorican', 'Amerindian'.
		</li>
		<li><b>Gender</b> The gender of the students has been categorised as either 
		Female (1) or Male (2).
		</li>
		</ul>


		<br><br><font size="6"> <span style="color:green">ML Model:</span><br>
		<font size="2">

		 A practitioner of machine learning may initially consider this data a good starting 
		 point for the creation of a model used to predict an individuals potential for 
		 success in law school. We can imagine such a model being used by an admissions 
		 department as part of the process for deciding who to accept into the program
		 and who to reject. Inputs such as GPA, LSAT and Sanders-Index on first impressions
		 appear to be objective and measurable ground truths reflecting real-world outcome 
		 and do not appear to be the result of an obviously subjective decision taken by 
		 a possibly prejudiced human. 
		 
		<br>
		   
		The data could, for example, be used to:
			<ul>
			<li>Create a model to predict the outcome of the first year of law school by using 'ZFYA'
			as the training target.
			<li>Create a model to predict the likelihood of passing the BAR exam by using 'first-fp' as the training target<br>
			</ul>

		The outcome of either of the above models might be a useful aid for admission decisions.
		A basic assumption might lead one to believe that the existence of such a model would
		remove any potential for human bias. However, if the data upon which this "unbiased" 
		model will be trained contains measurements and decisions defined or collected in a fundamentally
		unfair society any expectation that a resulting model would be inherently unbiased simply
		because it is made by an algorithm has proven to be unrealistic, or at a minimum 
		questionable. From a bias and prejudice mitigation perspective it is not sufficient
		to replace a human decision-maker with an automated model that has detected patterns 
		in historic decisions and outcomes as a grounding for its automated predictions. 
		Such a model may ultimately mirror the exact human behaviour and societal influences
		that one would expect it to mitigate. We cannot reasonably assume that the resulting 
		model will not reflect the subjectivity, personal bias or societal influences that have
		influenced the outcomes and decisions reflected in the training data. 



		<br>
		<b>If we detect:</b>
		<ul>
		<li>Disparities in the representation of groups within the sample data.</li>
		<li>Significant differences in the distribution of the quantifiable measurements across
		gender, race or any other protected attribute in the target(y).</li>
		<li>Significant differences in the distribution of the quantifiable measurements across gender, race or 
		  any other protected attribute in any of the training input features(X0 to Xn).</li>
		<li>Significant differences across protected features in the outcome of any 
		resulting trained model.</li>
		<li>Significant differences in the various measurements of accuracy employed to measure the overall accuracy of the trained model.</li>
		</ul>

		It is necessary to actively reflect upon and decide if the data should be used to train
		an automated decision-making model, and if the resulting model is fair, through various
		accuracy measurements and fairness definitions.

		<br><br><font size="6"> <span style="color:green">Considerations:</span><br>
		<font size="2">
		Below are some questions we may want to ask in terms of this particular dataset.
		Keeping in mind that for each dataset, the questions will be different. 
		The objective of using this sample dataset is not to categorically answer if
		or why such disparities exist, but rather to reiterate that reflection and
		research are required. This is particularly true when the model uses measurements
		of complex human characteristics such as intelligence, resilience or potential 
		which have been converted, by one means or another, to abstract quantities. 
		The creation of a predictive model in the context of law school education 
		can have severe consequences for individuals as well as for groups and entire
		societies. Fairness as a philosophy has no objective definition, and as such, 
		there is no consensus on a mathematical formulation. It is, therefore, necessary to 
		reflect upon the worldview or philosophy of fairness that the model will encompass, 
		that the creator of the model is comfortable to take ownership of and that the consumer
		of any such model is fully aware of before use. The use of the Machnamh framework will
		help to identify such disparities across protected groups and to prompt conversations
		about the philosophies of fairness the creators wish to reflect. 
		</b>.
		<br>

		If we follow the timelines of the educational path in the USA, which is reflected in this database, 
		the chronology of academic milestones and their corresponding measurements are, first
		the undergraduate grade point average(UGPA), followed by the LSAT which is the standardised 
		test necessary to enter into law school, then the grades obtained throughout law school as measured
		by the annual grade point average, in this case, we have access to the first-year grade point average,
		and finally the BAR exam, another standardised test which is necessary to finally
		practice law. 
		<br>

		<b>Grade point average (GPA) and First Year Average (FYA)</b> are based on the academic achievements of 
		students through class participation and teacher/professor exam and project grading.
		If we see significant disparities here in academic performance amongst protected groups we need to ask why,
		and to determine what worldview we standby concerning any such disparities. There is for example much
		evidence to suggest that certain student groups are disadvantaged, not solely due to socioeconomic 
		factors but also through the existence of both implicit teacher bias and stereotype threat(where 
		individuals feel themselves at risk of conforming to stereotypes about their social group, the pressure of 
		which affects performance). In the US and elsewhere, students of colour are significantly
		more likely to attend low-income schools with less qualified teachers, fewer resources, 
		larger classes sizes, and lower long-term expectations. See the 'further reading' 
		section for more details.<br>

		<b>LSAT and BAR exams</b> are both standardised tests, if we see significant disparities 
		here in academic performance amongst protected groups we need to ask why,
		and to determine what worldview we standby concerning any such disparities. Much debate
		has occurred over many decades concerning the fairness of such tests. Good GPA's alone will not ensure entry to
		the majority of law school which places huge importance on the LSAT and the more recent
		ACT standardised tests. Much discussion has revolved around the very origins of the LSAT
		given that standardized tests were introduced in the early 1920s by eugenicists
		with outspoken racist ideologies(Luis Terman one of the forefathers of the original IQ 
		test who believed that IQ was highly heritable, and Carl Brigham the primary developer of
		the SAT who also supported the "native intelligence" hypothesis). Birgham later, in the 1930s, publically reversed his position that American education was declining and "will proceed with an accelerating rate as the racial mixture becomes more and more extensive.". 
		This may, however, lead one to question if standardised tests are in general biased 
		towards the success of the group who have historically held the most power in any society,
		given that such tests have been developed and written in terms of the understandings of
		that privileged class based upon the world and the culture that facilitates this privilege.
		Due to LSAT disparities minority students on average end up attending lower-ranked law 
		schools, which often results in have higher debt burdens, lower employment rates, and 
		lower income levels. 

		<br>
		A cheating scandal surrounding standardised tests recently implicated several college
		administrators and celebrities. One result of this was a fourteen-day prison 
		sentence and a 30,000 USD fine based on the accused's admittance of paying 15,000 USD
		toward having incorrect SAT answers altered on behalf of her white, wealthy daughter.
		Another case in 2011 resulted in a black woman and her father being charged with
		felonies related to the theft of public education and a 10 year jail sentence, suspended down
		to 10 days. In this case the mother enroll her children in a school using their 
		grandfathers address. The result was a hop from a school in their own neighbourhood 
		which met 4 of the states 26 educational standards to a school in their grandfathers one
		which met all 26. This might lead one to question the role of socioeconomics in education and standardised test results.

		A quick google search also indicates that BAR preperation and SAT preparation courses are 
		generally offered at a costs of 2,000USD to 4000 USD (or 150 USD per hour for private tuition),
		does this already place those with socioeconomic difficulties at a more significant 
		disadvantage than those who can afford to take such preparation courses?


		<br>
		Other questions that might also be raised in terms of world view is if it is
		even valid to speculate that the act of passing the BAR exam on the first 
		attempt correlates with the release into the justice system of a skilled and 
		responsible lawyers with moral character, fitness and a committment to legal justice? 
		Are there other equally relevant skills which the BAR exam cannot measure?
		<br>

				
				
		<br><br><font size="6"> <span style="color:green">References and Further reading</span><br>
		<font size="2"> 

		<div style="padding-left: 4em; text-indent: -4em;">

		<p>A 2017 study from NYU Steinhardt has indicated that English and Math teachers underestimate the academic
		abilities of students of color, which in turn has an impact on students’ grades and academic expectations.
		</p>

		<p>
		A 2018 study from the University of Mannheim, Germany, found that pre-service teachers “graded the performance of a student who appeared to 
		have a migrant background statistically significantly worse than that of a student without 
		a migrant background.” Bonefeld, M., & Dickhäuser, O. (2018). (Biased) Grading of Students’ 
		performance: Students’ names, performance level, and implicit attitudes. 
		Frontiers in Psychology, 9(MAY). https://doi.org/10.3389/fpsyg.2018.00481


		<p>A 2002 Education Longitudinal Study found that “Teacher expectations were more predictive of college 
		success than most major factors, including student motivation and student effort.” Unconscious bias in teachers 
		towards protected groups(minorities, low income, women in STEM) may affect edducational outcomes and achievements.
		</p>

		<p>
		A 2006 study shows the fear of confirming a negative stereotype aimed at one's group could undermine academic performance
		in minority students by elevating their level of psychological threat.
		Cohen, G. L., Garcia, J., Apfel, N., & Master, A. (2006). Reducing the racial achievement gap:
		A social-psychological intervention. Science, 313(5791), 1307–1310. https://doi.org/10.1126/science.1128317
		</p>

		<p>An education study from Israel[B] indicated that gender bias affected how teachers graded female students, 
		even when the majority of teachers in the study were themselves female.
		Lavy, V., & Sand, E. (2018). On the origins of gender gaps in human capital: Short- and long-term 
		consequences of teachers’ biases. Journal of Public Economics, 167, 263–279. 
		https://doi.org/10.1016/j.jpubeco.2018.09.007
		</p>

		<p>A 2015 study suggest that teacher biase in early education has long term implications for 
		occupational choices and earnings. This impact being larger on girls from low socioeconomic background.
		Lavy, V., & Sand, E. (2015). On the origins of gender human capital gaps: short and long term consequences 
		of teachers’ stereotypical biases. NBER Working Paper, (January), 1–53. https://doi.org/10.3386/w20909
		</p>

		<p>
		A 2014 study indicates that Black and Latino boys face “disparities in access, opportunity, and achievement’
		’ that cause them to lag behind their peers in those areas and can diminish their opportunities later in life.
		P, M. H., Christina, M., Rosann, T., Ray, W., Dan, F., Sara, M., … University, A. (2014). 
		Opportunity and Equity: Enrollment and Outcomes of Black and Latino Males in Boston Public Schools.
		Annenberg Institute for School Reform at Brown University. 
		Retrieved from http://search.ebscohost.com/login.aspx?direct=true&db=eric&AN=ED553658&site=ehost-live
		</p>

		<p>
		A study mentioned in this Times article (along with mention of many other related studies) shows that 
		young black boys are most likely to be suspended and that black girls are disproportionately penalized 
		for being assertive in classroom settings. Black girls are twelve times more likely to be suspended and
		over policed than their white peers. 
		https://time.com/3705454/teachers-biases-girls-education/
		</p>

		<p>A 2014 report showed that black children although accounting for only 18% of preschoolers account for
		48% of children suspended more than once a seperat study suggests that teachers “increased the severity
		of suggested disciplinary actions when the race of the teachers didn’t match that of the child.” 
		This has a stronger impact on children of colour given that the majority of Teachers are still White.
		U.S. Department of Education Office for Civil Rights CIVIL RIGHTS DATA COLLECTION
		Data Snapshot: Early Childhood Education, Issue Brief No. 2 (March 2014) 
		https://www2.ed.gov/about/offices/list/ocr/docs/crdc-early-learning-snapshot.pdf
		</p>


		<p>Students gain entry into the specialized schools by acing a single exam that tests their 
		mastery of math and English. Only 7 Black Students Got Into Stuyvesant, N.Y.’s Most Selective High School, 
		Out of 895 Spots.
		https://www.nytimes.com/2019/03/18/nyregion/black-students-nyc-high-schools.html?auth=login-facebook
		</p>

		<p>
		There is a possibility that the SAT is racially biased indicating that the observed racial gap
		in the results which may lead to the overstating of the academic achievement gap.
		Reeves, R. V., & Halikias, D. (2017). Race gaps in SAT scores highlight inequality and 
		hinder upward mobility. The Brookings Institute. 
		Retrieved from https://www.brookings.edu/research/race-gaps-in-sat-scores-highlight-inequality-and-hinder-upward-mobility/
		</p>

		<p>
		Recent research has indicated that GPAs were found to be five times stronger than 
		ACT scores at predicting graduation rates, and that the effect of GPAs was consistent
		across schools, unlike ACT scores. 
		A. Allensworth, E. M., & Clark, K. (2020). High School GPAs and ACT Scores as Predictors of 
		College Completion: Examining Assumptions About Consistency Across High Schools. 
		Educational Researcher, 49(3), 198–211. https://doi.org/10.3102/0013189X20902110
		</p>

		<p>Race gaps in SAT scores highlight inequality and hinder upward mobility:
		https://www.brookings.edu/research/race-gaps-in-sat-scores-highlight-inequality-and-hinder-upward-mobility/
		</p>

		<p>
		Il)logical Reasoning: The LSAT’s Troubling History of Exclusion
		https://brownpoliticalreview.org/2019/12/illogical-reasoning-the-lsats-troubling-history-of-exclusion/
		</p>

		<p>In the early 20th century "The Association of American Law Schools, representing the
		more expensive, university-affiliated institutions, banded together with the American Bar Association 
		(ABA) to campaign for states to raise the requirements for aspiring lawyers. 
		The target: keeping minorities out of the profession."
		https://www.thenation.com/article/archive/law-schools-failing-students-color/
		</p>

		<p>
		Brigham, C. C. (1923). A study of American intelligence. Princeton University Press. 
		</p>

		<p>
		Leslie, B. (2000). Nicholas Lemann: “The Big Test: The Secret History of the 
		American Meritocracy.” American Studies in Scandinavia, 32(2), 
		97–101. https://doi.org/10.22439/asca.v32i2.2772
		</p>

		<p>
		Taylor, B. P. (2014). Testing Wars in the Public Schools: A Forgotten History. 
		Journal of American History, 100(4), 1197–1197. https://doi.org/10.1093/jahist/jau035
		</p>

		<p>
		In 2019 the American Bar Association reported that the racial breakdown of attorneys nationwide was 85% White, 
		5% Black, 5%, Latinx, 2% Asian, and 1% Native American with 36% identifying as Female and 64% identifying as Male
		[ABA National Lawyer Population Survey 10-Year Trend in Lawyer Demographics
		Year 2019]
		https://www.americanbar.org/content/dam/aba/administrative/market_research/national-lawyer-population-demographics-2009-2019.pdf
		</p>

		<p>
		The History of the SAT Is Mired in Racism and Elitism: It’s “proof of the miles we have left to reach social justice and liberation for all in this country.”
		https://www.teenvogue.com/story/the-history-of-the-sat-is-mired-in-racism-and-elitism
		</p>

		<p>
		Subotnik, D. (2013). Does Testing = Race Discrimination?: Ricci, the Bar Exam, the LSAT,
		and the Challenge to Learning. U. Mass. L. Rev, 8, 332.
		</p>

		<p>
		"Terman has been viewed as a sloppy thinker at best and a racist, sexist, and/or classist
		at worst. This article explores the most common criticisms of Terman’s legacy: 
		an overemphasis on IQ, support for the meritocracy, and emphasizing genetic 
		explanations for the origin of intelligence differences over environmental ones."
		Warne, R. T. (2019). An Evaluation (and Vindication?) of Lewis Terman: 
		What the Father of Gifted Education Can Teach the 21st Century. 
		Gifted Child Quarterly, 63(1), 3–21. https://doi.org/10.1177/0016986218799433
		</p>

		<p>
		How the largest college admissions scandal ever let wealthy parents cheat the system.
		https://www.latimes.com/local/lanow/la-me-college-admissions-fraud-scheme-20190313-story.html
		</p>

		<p>
		Factors Affecting Bar Passage Among Law Students: The REAL Connection between Race and 
		Bar Passage. The African American Attorney Network.
		https://aaattorneynetwork.com/factors-affecting-bar-passage-among-law-students-the-real-connection-between-race-and-bar-passage/

		</p>

		<p>
		Her Only Crime Was Helping Her Kids. Kelley Williams-Bolar, like Felicity Huffman, 
		was punished for trying to get her children a better education.
		https://www.theatlantic.com/ideas/archive/2019/09/her-only-crime-was-helping-her-kid/597979/
		</p>

		"""
