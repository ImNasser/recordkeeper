-- Query 1: List all Employees whose salary is between 1,000 AND 2,000. Show the Employee Name, Department and Salary
-- To list all employees with salary, and department name, a join was made between both tables.
-- Attributes were selected with table aliases, e for EMP and d for DEPT. In this case the join condition is dept no from both tables.
select e.ename,d.dname,e.sal from EMP e, DEPT d where e.DEPTNO=d.DEPTNO and e.SAL BETWEEN 1000 and 2000

-- Query 2: Count the number of people in department 30 who receive a salary and the number of people who receive a commission. 
-- In this case, an aggregate function was used to count the total number of employees of department 30. The aggregate function count was applied for employee table attribute salary. The reason is, we need to find the employees who receive a salary, we can use any other attribute, but must not be an attribute which can have null values. Three where clause conditions were supplied for this query
-- 1st: emp dept no=department dept no
-- 2nd: departmanet no=30
-- 3rd: commision is not null
-- All of these above conditions should be true for query to return results.
select COUNT(e.sal) from EMP e, DEPT d where e.DEPTNO=d.DEPTNO and d.DEPTNO=30 and e.COMM is NOT  NULL  

-- Query 3: Find the name and salary of employees in Dallas.
-- To find name and salary of employees, employee name and selected were selected and a join was made select COUNT(e.sal) from EMP e, DEPT d where e.DEPTNO=d.DEPTNO and d.DEPTNO=30 and e.COMM is NOT  NULL  (merged)between dept and emp tables. Also, a second where clause was specified with department location must be in Dallas.
select e.ENAME , e.SAL  from EMP e, DEPT d where e.DEPTNO=d.DEPTNO and d.LOC ="Dallas"


-- Query 4: List all departments that do not have any employees.
-- To list all departments names, department name was selected and to list department which do not have any employee a where clause was made using a second inner query. The inner query returns the deptno of all the employees. The outer query performs a where clause on the dept no column with the condition that dept no is not part of the inner query. This returns all the departments which do not have any employees.
select d.DNAME from DEPT d where d.DEPTNO not IN (select DEPTNO from EMP)


-- Query 5: List the department number and average salary of each department
-- For this query, department name and an employee average salary with the aggregate function avg was used, which calculates the average of the salary. To perform aggregation only on the employees of a specific department, a group by clause was used, which groups the results by dept no column.
-- Also, average salary was renamed as average_sal column in the results using the as keyword.
select d.DEPTNO, AVG(e.SAL) as average_Sal from EMP e,DEPT d where e.DEPTNO=d.DEPTNO group by d.DEPTNO 



